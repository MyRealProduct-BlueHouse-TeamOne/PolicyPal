import os
import json
import nltk
from nltk.tokenize import sent_tokenize
import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments, AutoModelForSeq2SeqLM, AutoTokenizer
import torch
from torch.utils.data import Dataset

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Download necessary NLTK data
nltk.download('punkt')

# Load each JSON object separately
data = []
with open('Datasets/dataset.json', 'r') as f:
    for line in f:
        pair = json.loads(line)

        # Generate bullet-pointed sentences for summary
        sentences = sent_tokenize(pair["summary"])
        bullet_summary = ["• " + sentence for sentence in sentences]
        formatted_summary = "\n".join(bullet_summary)

        # Add instruction-based prompt to plain text
        instruction_prompt = "Summarize the following terms of services in bullet points:\n\n"

        # Combine the instruction with the plain text
        combined_plain_text = instruction_prompt + pair['plain_text']

        # Append to data with the modified plain text and bullet-pointed summary
        data.append({
            "plain_text": combined_plain_text,
            "summary": formatted_summary
        })

print(f"Length of dataset 1: {len(data)}")

# Load your existing dataset
with open('Datasets/licenses_data.json', 'r') as file:
    data_1 = json.load(file)

# Process and transform the data into a simple format with prompt engineering
tos_summary_pairs = []
for link, content in data_1.items():
    full_tos = content.get('full_text')
    summary = content.get('terms')

    if full_tos and summary:
        # Add a prompt instruction to the plain_text
        instruction_prompt = "Summarize the following Terms of Service in bullet points so that each point is around 30 words max:\n\n"

        # Combine the instruction with the full text
        combined_plain_text = instruction_prompt + full_tos

        # Format the summary with bullet points
        bullet_summary = ["• " + term for term in summary]
        formatted_summary = "\n".join(bullet_summary)

        # Append to the list as a dictionary
        tos_summary_pairs.append({
            'plain_text': combined_plain_text,
            'summary': formatted_summary
        })

print(f"Length of dataset 2: {len(tos_summary_pairs)}")

data_new = data + tos_summary_pairs

print(f"Total data length: {len(data_new)}")

# Extract TOS documents and their summaries
texts = [item['plain_text'] for item in data_new]
summaries = [item['summary'] for item in data_new]

# Split the data into training and validation sets
train_texts, eval_texts, train_summaries, eval_summaries = train_test_split(
    texts, summaries, test_size=0.2, random_state=42
)

# Load the Pegasus-Large model and tokenizer
model_name = "sshleifer/distilbart-cnn-12-6"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Tokenize the datasets
train_inputs = tokenizer(train_texts, max_length=1024, truncation=True, padding=True, return_tensors="pt")
train_labels = tokenizer(train_summaries, max_length=256, truncation=True, padding=True, return_tensors="pt")

eval_inputs = tokenizer(eval_texts, max_length=1024, truncation=True, padding=True, return_tensors="pt")
eval_labels = tokenizer(eval_summaries, max_length=256, truncation=True, padding=True, return_tensors="pt")

# Adjust labels to ignore padding tokens in the loss calculation
train_labels["input_ids"][train_labels["input_ids"] == tokenizer.pad_token_id] = -100
eval_labels["input_ids"][eval_labels["input_ids"] == tokenizer.pad_token_id] = -100

# Ensure the data is also on the GPU (if necessary)
train_inputs = train_inputs.to(device)
train_labels = train_labels.to(device)
eval_inputs = eval_inputs.to(device)
eval_labels = eval_labels.to(device)


class TOSDataset(Dataset):
    def __init__(self, inputs, labels):
        self.inputs = inputs
        self.labels = labels

    def __len__(self):
        return len(self.inputs["input_ids"])

    def __getitem__(self, idx):
        item = {key: val[idx].to(device) for key, val in self.inputs.items()}
        item['labels'] = self.labels["input_ids"][idx].to(device)
        return item


# # Create dataset objects
train_dataset = TOSDataset(train_inputs, train_labels)
eval_dataset = TOSDataset(eval_inputs, eval_labels)

# Define training arguments
training_args = Seq2SeqTrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=1e-5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    weight_decay=0.01,
    save_total_limit=3,
    num_train_epochs=15,
    predict_with_generate=True,
    save_steps=500,
    logging_steps=100,
    fp16=True,  # Enable mixed precision if desired (faster training on compatible GPUs)
)

# Initialize the trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer
)

trainer.train()

# Save the model and tokenizer
trainer.save_model("distilbart")
tokenizer.save_pretrained("distilbart")

# Define the path to the saved model and tokenizer
model_path = "distilbart"

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

# Prepare the model for evaluation
model.eval()

# Example TOS document for inference
new_tos = """Summarize the following Terms of Service in bullet points:\n\nThanks for using Dropbox! These terms of service ("Terms") cover your use and access to the services, client software and websites ("Services") provided by Dropbox, Inc. Our Privacy Policy explains how we collect and use your information while our Acceptable Use Policy outlines your responsibilities when using our Services. By using our Services, you're agreeing to be bound by these Terms, and to review our Privacy and Acceptable Use policies. If you're using our Services for an organization, you're agreeing to these Terms on behalf of that organization.

Your Stuff & Your Permissions
When you use our Services, you provide us with things like your files, content, email messages, contacts and so on ("Your Stuff"). Your Stuff is yours. These Terms don't give us any rights to Your Stuff except for the limited rights that enable us to offer the Services.

We need your permission to do things like hosting Your Stuff, backing it up, and sharing it when you ask us to. Our Services also provide you with features like photo thumbnails, document previews, email organization, easy sorting, editing, sharing and searching. These and other features may require our systems to access, store and scan Your Stuff. You give us permission to do those things, and this permission extends to trusted third parties we work with.

Sharing Your Stuff
Our Services let you share Your Stuff with others, so please think carefully about what you share.

Your Responsibilities
You're responsible for your conduct, Your Stuff and you must comply with our Acceptable Use Policy. Content in the Services may be protected by others' intellectual property rights. Please don't copy, upload, download or share content unless you have the right to do so.

We may review your conduct and content for compliance with these Terms and our Acceptable Use Policy. With that said, we have no obligation to do so. We aren't responsible for the content people post and share via the Services.

Please safeguard your password to the Services, make sure that others don't have access to it, and keep your account information current.

Finally, our Services are not intended for and may not be used by people under the age of 13. By using our Services, you are representing to us that you're over 13.

Software
Some of our Services allow you to download client software ("Software") which may update automatically. So long as you comply with these Terms, we give you a limited, nonexclusive, nontransferable, revocable license to use the Software, solely to access the Services. To the extent any component of the Software may be offered under an open source license, we'll make that license available to you and the provisions of that license may expressly override some of these Terms. Unless the following restrictions are prohibited by law, you agree not to reverse engineer or decompile the Services, attempt to do so, or assist anyone in doing so.

Our Stuff
The Services are protected by copyright, trademark, and other US and foreign laws. These Terms don't grant you any right, title or interest in the Services, others' content in the Services, Dropbox trademarks, logos and other brand features. We welcome feedback, but note that we may use comments or suggestions without any obligation to you.

Copyright
We respect the intellectual property of others and ask that you do too. We respond to notices of alleged copyright infringement if they comply with the law, and such notices should be reported using our DMCA Process. We reserve the right to delete or disable content alleged to be infringing and terminate accounts of repeat infringers. Our designated agent for notice of alleged copyright infringement on the Services is:

Copyright Agent
Dropbox, Inc.
185 Berry Street, Suite 400
San Francisco, CA 94107
copyright@dropbox.com

Paid Accounts
Billing. You can increase your storage space and add paid features to your account (turning your account into a "Paid Account"). We'll automatically bill you from the date you convert to a Paid Account and on each periodic renewal until cancellation. You're responsible for all applicable taxes, and we'll charge tax when required to do so.

No Refunds. You may cancel your Dropbox Paid Account at any time but you won't be issued a refund.

Downgrades. Your Paid Account will remain in effect until it's cancelled or terminated under these Terms. If you don't pay for your Paid Account on time, we reserve the right to suspend it or reduce your storage to free space levels. You're responsible for all taxes, and we may charge taxes when required to do so.

Changes. We may change the fees in effect but will give you advance notice of these changes via a message to the email address associated with your account.

Dropbox for Business
Email address. If you sign up for a Dropbox account with an email address provisioned by your employer, your employer may be able to block your use of Dropbox until you transition to a Dropbox for Business account or you associate your Dropbox account with a personal email address.

Using Dropbox for Business. If you join a Dropbox for Business account, you must use it in compliance with your employer's terms and policies. Please note that Dropbox for Business accounts are subject to your employer's control. Your administrators may be able to access, disclose, restrict, or remove information in or from your Dropbox for Business account. They may also be able to restrict or terminate your access to a Dropbox for Business account. If you convert an existing Dropbox account into a Dropbox for Business account, your administrators may prevent you from later disassociating your account from the Dropbox for Business account.

Termination
You're free to stop using our Services at any time. We also reserve the right to suspend or end the Services at any time at our discretion and without notice. For example, we may suspend or terminate your use of the Services if you're not complying with these Terms, or use the Services in a manner that would cause us legal liability, disrupt the Services or disrupt others' use of the Services. Except for Paid Accounts, we reserve the right to terminate and delete your account if you haven't accessed our Services for 12 consecutive months. We'll of course provide you with notice via the email address associated with your account before we do so.

Services "AS IS"
We strive to provide great Services, but there are certain things that we can't guarantee. TO THE FULLEST EXTENT PERMITTED BY LAW, DROPBOX AND ITS AFFILIATES, SUPPLIERS AND DISTRIBUTORS MAKE NO WARRANTIES, EITHER EXPRESS OR IMPLIED, ABOUT THE SERVICES. THE SERVICES ARE PROVIDED "AS IS." WE ALSO DISCLAIM ANY WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. Some states don't allow the disclaimers in this paragraph, so they may not apply to you.

Limitation of Liability
TO THE FULLEST EXTENT PERMITTED BY LAW, IN NO EVENT WILL DROPBOX, ITS AFFILIATES, SUPPLIERS OR DISTRIBUTORS BE LIABLE FOR (A) ANY INDIRECT, SPECIAL, INCIDENTAL, PUNITIVE, EXEMPLARY OR CONSEQUENTIAL DAMAGES OR ANY LOSS OF USE, DATA, BUSINESS, OR PROFITS, REGARDLESS OF LEGAL THEORY, WHETHER OR NOT DROPBOX HAS BEEN WARNED OF THE POSSIBILITY OF SUCH DAMAGES, AND EVEN IF A REMEDY FAILS OF ITS ESSENTIAL PURPOSE; (B) AGGREGATE LIABILITY FOR ALL CLAIMS RELATING TO THE SERVICES MORE THAN THE GREATER OF $20 OR THE AMOUNTS PAID BY YOU TO DROPBOX FOR THE PAST 12 MONTHS OF THE SERVICES IN QUESTION. Some states don't allow the types of limitations in this paragraph, so they may not apply to you.

Resolving Disputes
Let's Try To Sort Things Out First. We want to address your concerns without needing a formal legal case. Before filing a claim against Dropbox, you agree to try to resolve the dispute informally by contacting dispute-notice@dropbox.com. We'll try to resolve the dispute informally by contacting you via email. If a dispute is not resolved within 15 days of submission, you or Dropbox may bring a formal proceeding.

We Both Agree To Arbitrate. You and Dropbox agree to resolve any claims relating to these Terms or the Services through final and binding arbitration, except as set forth under Exceptions to Agreement to Arbitrate below.

Opt-out of Agreement to Arbitrate. You can decline this agreement to arbitrate by clicking here and submitting the opt-out form within 30 days of first accepting these Terms.

Arbitration Procedures. The American Arbitration Association (AAA) will administer the arbitration under its Commercial Arbitration Rules and the Supplementary Procedures for Consumer Related Disputes. The arbitration will be held in the United States county where you live or work, San Francisco (CA), or any other location we agree to.

Arbitration Fees and Incentives. The AAA rules will govern payment of all arbitration fees. Dropbox will pay all arbitration fees for claims less than $75,000. If you receive an arbitration award that is more favorable than any offer we make to resolve the claim, we will pay you $1,000 in addition to the award. Dropbox will not seek its attorneys' fees and costs in arbitration unless the arbitrator determines that your claim is frivolous.

Exceptions to Agreement to Arbitrate. Either you or Dropbox may assert claims, if they qualify, in small claims court in San Francisco (CA) or any United States county where you live or work. Either party may bring a lawsuit solely for injunctive relief to stop unauthorized use or abuse of the Services, or intellectual property infringement (for example, trademark, trade secret, copyright, or patent rights) without first engaging in arbitration or the informal dispute-resolution process described above.

No Class Actions. You may only resolve disputes with us on an individual basis, and may not bring a claim as a plaintiff or a class member in a class, consolidated, or representative action. Class arbitrations, class actions, private attorney general actions, and consolidation with other arbitrations aren't allowed.

Judicial forum for disputes. In the event that the agreement to arbitrate is found not to apply to you or your claim, you and Dropbox agree that any judicial proceeding (other than small claims actions) will be brought in the federal or state courts of San Francisco County (CA). Both you and Dropbox consent to venue and personal jurisdiction there.

Controlling Law
These Terms will be governed by California law except for its conflicts of laws principles.

Entire Agreement
These Terms constitute the entire agreement between you and Dropbox with respect to the subject matter of these Terms, and supersede and replace any other prior or contemporaneous agreements, or terms and conditions applicable to the subject matter of these Terms. These Terms create no third party beneficiary rights.

Waiver, Severability & Assignment
Dropbox's failure to enforce a provision is not a waiver of its right to do so later. If a provision is found unenforceable, the remaining provisions of the Terms will remain in full effect and an enforceable term will be substituted reflecting our intent as closely as possible. You may not assign any of your rights under these Terms, and any such attempt will be void. Dropbox may assign its rights to any of its affiliates or subsidiaries, or to any successor in interest of any business associated with the Services.

Modifications
We may revise these Terms from time to time, and will always post the most current version on our website. If a revision meaningfully reduces your rights, we will notify you (by, for example, sending a message to the email address associated with your account, posting on our blog or on this page). By continuing to use or access the Services after the revisions come into effect, you agree to be bound by the revised Terms."""

# Tokenize the input text
inputs = tokenizer(new_tos, max_length=1024, truncation=True, return_tensors="pt")

# Generate the summary
summary_ids = model.generate(
    inputs["input_ids"],
    max_length=400,
    min_length=50,
    length_penalty=1.0,
    num_beams=10,
    early_stopping=True
)

import time
start = time.time()
# Decode the summary
summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

last_punctuation = max(summary.rfind('.'), summary.rfind('!'), summary.rfind('?'))
if last_punctuation != -1:
    summary = summary[:last_punctuation + 1]

print("Generated Summary:")
print(summary)
print((time.time()-start)/60)
