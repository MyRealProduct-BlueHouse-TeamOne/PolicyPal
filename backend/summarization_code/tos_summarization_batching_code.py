# Original file is located at
#     https://colab.research.google.com/drive/1PRzmAeab7cDntg16z2GGw6IXlqaYVSkN

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import nltk
from nltk.tokenize import sent_tokenize

# # Download nltk data
nltk.download('punkt')
import time

# start_time = time.time()

# Load model and tokenizer
model_name = "sshleifer/distilbart-cnn-12-6"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Set device to CPU or CUDA
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def chunk_text(text, max_length):
    """Chunks the text into smaller pieces that fit within the model's max input length."""
    tokens = tokenizer(text, return_tensors='pt', truncation=False)['input_ids'][0]
    chunks = []
    for i in range(0, len(tokens), max_length):
        chunk = tokens[i:i+max_length]
        chunks.append(tokenizer.decode(chunk, skip_special_tokens=True))
    return chunks

def batch_inference(chunks, batch_size=4, max_length=1024):
    """Performs inference on a batch of text chunks."""
    all_summaries = []

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]

        inputs = tokenizer(batch, return_tensors="pt", max_length=max_length, truncation=True, padding=True).to(device)

        # Generate summaries for the batch
        with torch.no_grad():
            summary_ids = model.generate(
                inputs["input_ids"],
                max_length=150,
                min_length=60,
                length_penalty=2.0,
                num_beams=4,
                early_stopping=True
            )

        # Decode summaries and add to list
        summaries = [tokenizer.decode(s, skip_special_tokens=True) for s in summary_ids]
        all_summaries.extend(summaries)

    return all_summaries

def summarize_text(text, max_length=1024, batch_size=4):
    """Summarizes the given text using chunking and batch inference."""
    # Chunk the text if it's too long
    chunks = chunk_text(text, max_length)

    # Perform batch inference
    summaries = batch_inference(chunks, batch_size=batch_size, max_length=max_length)

    # Combine the summaries
    combined_summary = " ".join(summaries)

    if len(tokenizer(combined_summary)['input_ids']) > max_length:
        inputs = tokenizer(combined_summary, return_tensors="pt", max_length=max_length, truncation=True).to(device)
        with torch.no_grad():
            final_summary_ids = model.generate(inputs["input_ids"], max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
        return tokenizer.decode(final_summary_ids[0], skip_special_tokens=True)

    # Split combined summary into sentences
    sentences = sent_tokenize(combined_summary)

    return sentences

# Example usage
long_text = """Thanks for using Dropbox! Our mission is to create a more enlightened way of working, and help you and those you work with stay coordinated. We do so by providing an intuitive, unified platform and suite of apps and services that keep your content safe, accessible and in sync. These terms of service (“Terms”) cover your use and access to our services, client software and websites ("Services"). If you reside outside of the United States of America, Canada and Mexico (“North America”) your agreement is with Dropbox International Unlimited Company. If you reside in North America your agreement is with Dropbox, Inc. Our Privacy Policy explains how we collect and use your information while our Acceptable Use Policy outlines your responsibilities when using our Services. By using our Services, you’re agreeing to be bound by these Terms, our Privacy Policy, and Acceptable Use Policy.

Your Stuff & Your Permissions

When you use our Services, you provide us with things like your files, content, messages, contacts, and so on (“Your Stuff”). Your Stuff is yours. These Terms don’t give us any rights to Your Stuff except for the limited rights that enable us to offer the Services.

You may need to register for an account to access the Services, and we may create an account for you so that you can interact with the Services.

Our Services include a suite of apps and websites. To help you stay productive, when you use the same account to access different parts of the suite, Your Stuff may come with you.

We need your permission to do things like hosting Your Stuff, backing it up, and sharing it when you ask us to. Our Services also provide you with features like commenting, sharing, searching, image thumbnails, document previews, optical character recognition (OCR), easy sorting and organization, and personalization to help reduce busywork. To provide these and other features, Dropbox accesses, stores, and scans Your Stuff. You give us permission to do those things, and this permission extends to our affiliates and trusted third parties we work with.

Your Responsibilities

Your use of our Services must comply with our Acceptable Use Policy. Content in the Services may be protected by others’ intellectual property rights. Please don’t copy, upload, download, or share content unless you have the right to do so.

Dropbox may review your conduct and content for compliance with these Terms and our Acceptable Use Policy. We aren’t responsible for the content people post and share via the Services.

Help us keep Your Stuff protected. Safeguard your password to the Services, and keep your account information current. Don’t share your account credentials or give others access to your account.

You may use our Services only as permitted by applicable law, including export control laws and regulations. Finally, to use our Services, you must be at least 13 if you reside in the United States, and 16 if you reside anywhere else. If the law where you reside requires that you must be older in order for Dropbox to lawfully provide the Services to you without parental consent (including use of your personal data), then you must be that older age.

Software

Some of our Services allow you to download client software (“Software”) which may update automatically. So long as you comply with these Terms, we give you a limited, nonexclusive, nontransferable, revocable license to use the Software, solely to access the Services. To the extent any component of the Software may be offered under an open source license, we’ll make that license available to you and the provisions of that license may expressly override some of these Terms. Unless the following restrictions are prohibited by law, you agree not to reverse engineer or decompile the Services, attempt to do so, or assist anyone in doing so.

Beta Services

We sometimes release products and features that we’re still testing and evaluating (“Beta Services”). Beta Services are labeled “alpha,” “beta,” “preview,” “early access,” or “evaluation” (or with words or phrases with similar meanings) and may not be as reliable as Dropbox’s other services. Beta Services are made available so that we can collect user feedback, and by using our Beta Services, you agree that we may contact you to collect such feedback.

Beta Services are confidential until official launch. If you use any Beta Services, you agree not to disclose any information about those Services to anyone else without our permission.

Electronic Signatures

By using a part of the Services that facilitates electronic signatures, you agree to do business electronically and to use electronic records and signatures. There may be laws where you reside governing what types of documents and transactions are appropriate for such signatures. It’s your responsibility to ensure that the electronic signature functionality provided by the Services is appropriate for your scenario. If the Services include sample documents (like a template NDA), these documents are for informational purposes only.

Fax Services

If you use a part of the Services that facilitates faxing, you may be required to provide information such as your name, billing address, physical address, payment information (including credit card number), and national ID number (where applicable). Failure to provide this information could result in suspension of your access.

You may not use our Services to send unsolicited fax advertisements or spam, and we may decide to not deliver any messages we consider unsolicited fax advertisements or spam.

We cannot guarantee that any particular fax number will be available for you to use. If you stop using our fax services, your number may be released or reassigned to another customer. In the US, UK, and Canada, we may support porting a fax number (both in and out) for an additional fee.

Additional Features

From time to time, Dropbox will add additional features to enhance the user experience of our storage service at no additional charge. However, these free features may be withdrawn without further notice.

Third-Party Features

The Services may give you the option to link to third-party features and integrations. Dropbox does not own or operate any such features or integrations.  If you access or use any third-party features or integrations, you are responsible for this access and use, and Dropbox is not responsible for any act or omission of the third party or the availability, accuracy, the related content, products or services of third parties.

Our Stuff

The Services are protected by copyright, trademark, and other US and foreign laws. These Terms don’t grant you any right, title, or interest in the Services, others’ content in the Services, Dropbox trademarks, logos and other brand features. We welcome feedback, but note that we may use comments or suggestions without any obligation to you.

Copyright

We respect the intellectual property of others and ask that you do too. We respond to notices of alleged copyright infringement if they comply with the law, and such notices should be reported using our Copyright Policy. We reserve the right to delete or disable content alleged to be infringing and terminate accounts of repeat infringers. Copyright infringement claims should be submitted using our Copyright Complaint Form or submitted to our designated agent for our Services at:

Copyright Agent
Dropbox, Inc.
1800 Owens St
San Francisco, CA 94158
copyright@dropbox.com

Paid Accounts

Billing. You can increase your storage space and add paid features to your account (turning your account into a “Paid Account”). We’ll automatically bill you from the date you convert to a Paid Account and on each periodic renewal until cancellation. If you’re on an annual plan, we’ll send you a notice email reminding you that your plan is about to renew within a reasonable period of time prior to the renewal date. You’re responsible for all applicable taxes, and we’ll charge tax when required to do so. Some countries have mandatory local laws regarding your cancellation rights, and this paragraph doesn’t override these laws.

Cancellation. You may cancel your Paid Account at any time. Refunds are only issued if required by law. For example, users living in the European Union have the right to cancel their Paid Account subscriptions and obtain a refund within 14 days of signing up for, upgrading to, or renewing a Paid Account by clicking here.

Downgrades. Your Paid Account will remain in effect until it's cancelled or terminated under these Terms. If you’re on a Dropbox Family plan, the Family manager may be able to downgrade your account at any time. If you don’t pay for your Paid Account on time, we reserve the right to suspend it or remove Paid Account features.

Changes. We may change the fees in effect on renewal of your subscription, to reflect factors such as changes to our product offerings, changes to our business, or changes in economic conditions. We’ll give you no less than 30 days’ advance notice of these changes via a message to the email address associated with your account and you’ll have the opportunity to cancel your subscription before the new fee comes into effect.

Dropbox Teams

Email address. If you sign up for a Dropbox account with an email address provisioned by your organization, your organization may be able to block your use of Dropbox until you transition to an account on a Dropbox Standard, Advanced, Enterprise, Education, or other team (collectively, “Dropbox Team”) or you associate your Dropbox account with a personal email address.

Using Dropbox Teams. If you join a Dropbox Team, you must use it in compliance with your organization’s terms and policies. Please note that Dropbox Team accounts are subject to your organization's control. Your administrators may be able to access, disclose, restrict, or remove information in or from your Dropbox Team account. They may also be able to restrict or terminate your access to a Dropbox Team account. If you convert an existing Dropbox account into part of a Dropbox Team, your administrators may prevent you from later disassociating your account from the Dropbox Team.

Termination

You’re free to stop using our Services at any time. We reserve the right to suspend or terminate your access to the Services with notice to you if Dropbox reasonably believes:

you’re in breach of these Terms,
your use of the Services would cause a real risk of harm or loss to us or other users, or
you don’t have a Paid Account and haven't accessed our Services for 12 consecutive months.
We’ll provide you with reasonable advance notice via the email address associated with your account to remedy the activity that prompted us to contact you and give you the opportunity to export Your Stuff from our Services. If after such notice you fail to take the steps we ask of you, we’ll terminate or suspend your access to the Services.

We won’t provide notice or an opportunity to export Your Stuff before termination or suspension of access to the Services where Dropbox reasonably believes:

you’re in material breach of these Terms, which includes, but is not limited to, violating our Acceptable Use Policy,
doing so would cause us legal liability or compromise our ability to provide the Services to our other users, or
we're prohibited from doing so by law.
Once we suspend or terminate your access to the Services, you will not be able to access or export Your Stuff. Dropbox does not provide refunds if we suspend or terminate your access to the Services, unless required by law.

Discontinuation of Services

We may decide to discontinue the Services in response to exceptional unforeseen circumstances, events beyond Dropbox’s control (for example a natural disaster, fire, or explosion), or to comply with a legal requirement. If we do so, we’ll give you reasonable prior notice so that you can export Your Stuff from our systems (we will give you no less than 30 days’ notice where possible under the circumstances). If we discontinue the Services in this way before the end of any fixed or minimum term you have paid us for, we’ll refund the portion of the fees you have pre-paid but haven't received Services for.

Services “AS IS”

We strive to provide great Services, but there are certain things that we can't guarantee. TO THE FULLEST EXTENT PERMITTED BY LAW, DROPBOX AND ITS AFFILIATES, SUPPLIERS AND DISTRIBUTORS MAKE NO WARRANTIES, EITHER EXPRESS OR IMPLIED, ABOUT THE SERVICES. THE SERVICES ARE PROVIDED "AS IS." WE ALSO DISCLAIM ANY WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. Some places don’t allow the disclaimers in this paragraph, so they may not apply to you. For example, these disclaimers do not override the legal protections, including statutory warranties, granted to consumers by EU law.

Limitation of Liability

WE DON’T EXCLUDE OR LIMIT OUR LIABILITY TO YOU WHERE IT WOULD BE ILLEGAL TO DO SO—THIS INCLUDES ANY LIABILITY FOR DROPBOX’S OR ITS AFFILIATES’ FRAUD OR FRAUDULENT MISREPRESENTATION IN PROVIDING THE SERVICES. IN COUNTRIES WHERE THE FOLLOWING TYPES OF EXCLUSIONS AREN’T ALLOWED, WE'RE RESPONSIBLE TO YOU ONLY FOR LOSSES AND DAMAGES THAT ARE A REASONABLY FORESEEABLE RESULT OF OUR FAILURE TO USE REASONABLE CARE AND SKILL OR OUR BREACH OF OUR CONTRACT WITH YOU. THIS PARAGRAPH DOESN’T AFFECT CONSUMER RIGHTS THAT CAN'T BE WAIVED OR LIMITED BY ANY CONTRACT OR AGREEMENT. IF YOU ARE AN EU OR UK CONSUMER, THESE TERMS DO NOT EXCLUDE DROPBOX’S LIABILITY FOR LOSSES AND DAMAGES THAT ARE A RESULT OF OUR FAILURE TO USE REASONABLE CARE AND SKILL IN PROVIDING THE SERVICES OR OF OUR BREACH OF OUR CONTRACT WITH YOU, AS LONG AS THOSE LOSSES AND DAMAGES ARE REASONABLY FORESEEABLE.

IN COUNTRIES WHERE EXCLUSIONS OR LIMITATIONS OF LIABILITY ARE ALLOWED, DROPBOX, ITS AFFILIATES, SUPPLIERS OR DISTRIBUTORS WON’T BE LIABLE FOR:

ANY INDIRECT, SPECIAL, INCIDENTAL, PUNITIVE, EXEMPLARY, OR CONSEQUENTIAL DAMAGES, OR
ANY LOSS OF USE, DATA, BUSINESS, OR PROFITS, REGARDLESS OF LEGAL THEORY.
THESE EXCLUSIONS OR LIMITATIONS WILL APPLY REGARDLESS OF WHETHER OR NOT DROPBOX OR ANY OF ITS AFFILIATES HAS BEEN WARNED OF THE POSSIBILITY OF SUCH DAMAGES.

IF YOU USE THE SERVICES FOR ANY COMMERCIAL, BUSINESS, OR RE-SALE PURPOSE, DROPBOX, ITS AFFILIATES, SUPPLIERS OR DISTRIBUTORS WILL HAVE NO LIABILITY TO YOU FOR ANY LOSS OF PROFIT, LOSS OF BUSINESS, BUSINESS INTERRUPTION, OR LOSS OF BUSINESS OPPORTUNITY. DROPBOX AND ITS AFFILIATES AREN’T RESPONSIBLE FOR THE CONDUCT, WHETHER ONLINE OR OFFLINE, OF ANY USER OF THE SERVICES.

OTHER THAN FOR THE TYPES OF LIABILITY WE CANNOT LIMIT BY LAW (AS DESCRIBED IN THIS SECTION), WE LIMIT OUR LIABILITY TO YOU TO THE GREATER OF $20 USD OR 100% OF ANY AMOUNT YOU'VE PAID UNDER YOUR CURRENT SERVICE PLAN WITH DROPBOX. THIS PROVISION DOES NOT APPLY TO EU CONSUMERS WHERE PROHIBITED BY APPLICABLE LAW.

Resolving Disputes

Let’s Try to Sort Things Out First. We want to address your concerns without needing a formal legal case. Before filing a claim against Dropbox, you agree to try to resolve the dispute informally by sending us a written Notice of Dispute at dispute-notice@dropbox.com that includes your name, a detailed description of the dispute, and the relief you seek. We’ll try to resolve the dispute informally by contacting you via email. If a dispute is not resolved within 60 days after submission, you or Dropbox may bring a formal proceeding. If you reside in the EU, the European Commission provides for an online dispute resolution platform, which you can access here: https://ec.europa.eu/consumers/odr.

Judicial Forum for Disputes. You and Dropbox agree that any judicial proceeding to resolve claims relating to these Terms or the Services will be brought in the federal or state courts of San Francisco County, California, subject to the mandatory arbitration provisions below. Both you and Dropbox consent to venue and personal jurisdiction in such courts. If you reside in a country (for example, a member state of the European Union) with laws that give consumers the right to bring disputes in their local courts, this paragraph doesn’t affect those requirements.

IF YOU’RE A U.S. RESIDENT, YOU ALSO AGREE TO THE FOLLOWING MANDATORY ARBITRATION PROVISIONS:

We Both Agree to Arbitrate. You and Dropbox agree to resolve any claims relating to or arising out of these Terms or the Services through final and binding individual arbitration by a single arbitrator, except as set forth under the “Exceptions to Agreement to Arbitrate” below. This includes disputes arising out of or relating to the interpretation or application of this “Mandatory Arbitration Provisions” section, including its scope, enforceability, revocability, or validity. The arbitrator may award relief only individually and only to the extent necessary to redress your individual claim(s); the arbitrator may not award relief on behalf of others or the general public.

Opt out of Agreement to Arbitrate. You can decline this agreement to arbitrate by clicking here and submitting the opt-out form within 30 days of first registering your account or agreeing to these Terms. However, if you agreed to a previous version of these Terms that allowed you to opt out of arbitration, your previous choice to opt out or not opt out remains binding.

Arbitration Procedures. The American Arbitration Association (AAA) will administer the arbitration under its Consumer Arbitration Rules. The AAA’s rules and filing instructions are available at www.adr.org or by calling 1-800-778-7879. The arbitration will be held in the United States county where you live or work, San Francisco (CA), or any other location we agree to.

Arbitration Fees and Incentives. The AAA rules will govern payment of all arbitration fees. For individual arbitration of non-frivolous claims less than $75,000 for which you timely provided Dropbox with a Notice of Dispute, Dropbox will reimburse arbitration filing fees at the conclusion of the arbitration and will pay other arbitration fees. For all other claims, the costs and fees of arbitration shall be allocated in accordance with the arbitration provider’s rules, including rules regarding frivolous or improper claims. If you receive an arbitration award that is more favorable than any offer we make to resolve the claim, we will pay you $1,000 in addition to the award. Dropbox will not seek its attorneys' fees and costs in arbitration unless the arbitrator determines that your claim is frivolous or brought for an improper purpose.

Exceptions to Agreement to Arbitrate. Either you or Dropbox may assert claims, if they qualify, in small claims court in San Francisco (CA) or any United States county where you live or work. Either party may bring a lawsuit solely for injunctive relief to stop unauthorized use or abuse of the Services, or intellectual property infringement (for example, trademark, trade secret, copyright, or patent rights) without first engaging in arbitration or the informal dispute-resolution process described above. If the agreement to arbitrate is found not to apply to you or your claim, you agree to the exclusive jurisdiction of the state and federal courts in San Francisco County, California to resolve your claim.

NO CLASS OR REPRESENTATIVE ACTIONS. You may only resolve disputes with us on an individual basis, and may not bring a claim as a plaintiff or a class member in a class, consolidated, or representative action. Class arbitrations, class actions, private attorney general actions, and consolidation with other arbitrations aren’t allowed.

Severability. If any part of this “Mandatory Arbitration Provisions” section is found to be illegal or unenforceable, the remainder will remain in effect, except that if a finding of partial illegality or unenforceability would allow class or representative arbitration, this “Mandatory Arbitration Provisions” section will be unenforceable in its entirety. If you are found to have a non-waivable right to bring a particular claim or to request a particular form of relief that the arbitrator lacks authority to redress or award according to this “Mandatory Arbitration Provisions” section, including public injunctive relief, then only that respective claim or request for relief may be brought in court, and you and we agree that litigation of any such claim or request for relief shall be stayed pending the resolution of any individual claim(s) or request(s) for relief in arbitration.

Controlling Law

These Terms will be governed by California law except for its conflicts of laws principles. However, some countries (including those in the European Union) have laws that require agreements to be governed by the local laws of the consumer's country. This paragraph doesn’t override those laws.

Entire Agreement

These Terms constitute the entire agreement between you and Dropbox with respect to the subject matter of these Terms, and supersede and replace any other prior or contemporaneous agreements, or terms and conditions applicable to the subject matter of these Terms. Our past, present, and future affiliates and agents can invoke our rights under this agreement in the event they become involved in a dispute with you. Otherwise, these Terms do not give rights to any third parties.

Waiver, Severability & Assignment

Dropbox’s failure to enforce a provision is not a waiver of its right to do so later. If a provision is found unenforceable, the remaining provisions of the Terms will remain in full effect and an enforceable term will be substituted reflecting our intent as closely as possible. You may not assign any of your rights under these Terms, and any such attempt will be void. Dropbox may assign its rights to any of its affiliates or subsidiaries, or to any successor in interest of any business associated with the Services.

Modifications

We may revise these Terms to better reflect:

changes to the law,
new regulatory requirements, or
improvements or enhancements made to our Services.
If an update affects your use of the Services or your legal rights as a user of our Services, we’ll notify you prior to the update's effective date by sending an email to the email address associated with your account or via an in-product notification. These updated terms will be effective no less than 30 days from when we notify you.

If you don’t agree to the updates we make, please cancel your account and stop using the Services before the updated Terms become effective. Where applicable, we’ll offer you a prorated refund based on the amounts you have prepaid for Services and your account cancellation date. By continuing to use or access the Services after the updates come into effect, you agree to be bound by the revised Terms.

Dropbox"""
sentences = summarize_text(long_text, max_length=1024, batch_size=4) # this returns summary as a list of sentences
# print(sentences)

for sentence in sentences:
    print(sentence)

# end_time = time.time()
# print(f"Execution time: {end_time - start_time} seconds")


