
const link = document.createElement('link');
link.href = chrome.runtime.getURL('../styles.css');
link.rel = 'stylesheet';
document.head.appendChild(link);

const bodyText=document.body.innerText;

//const summarizedText=await summarize(bodyText)
const sampleText="Lorem ipsum odor amet, consectetuer adipiscing elit. Velit a nunc per ultrices ac facilisi in semper. Lacinia malesuada ac magna neque adipiscing aenean gravida? Pharetra donec lacus, laoreet erat donec finibus consectetur. Lectus malesuada semper tristique amet aenean taciti lorem diam. Vitae vehicula tempus donec pharetra pulvinar diam quis faucibus. Lacinia fames vel mattis consectetur risus. Senectus justo faucibus ad facilisis proin eleifend. Vitae urna nascetur turpis turpis parturient feugiat nam. Tempus justo efficitur enim duis mauris auctor tellus eu. Platea arcu pharetra pulvinar vestibulum montes dapibus diam. Ante luctus blandit sagittis elit commodo nulla felis. Pellentesque ornare mus habitant felis tempus. Ligula class turpis et consequat nam. Consequat tellus consectetur penatibus semper nulla lectus. Aptent dictum sodales proin fusce egestas congue ridiculus tortor ex. Etiam imperdiet ex suspendisse neque non ornare mus facilisis. Bibendum efficitur augue, lobortis lobortis iaculis urna tortor. Phasellus eros id ut ut suspendisse. Aliquam interdum ut vitae aptent vitae etiam. Bibendum fusce feugiat fringilla arcu consequat ornare habitasse. Purus natoque quis commodo; penatibus donec potenti. Tempus fusce duis metus fusce enim justo nascetur tellus eleifend. Ultrices cras convallis sit ultricies aenean nec luctus. Lectus ultricies et viverra conubia, quam nostra sodales conubia. Conubia eros nascetur et, libero ridiculus id nec consequat. Ornare mollis sollicitudin bibendum luctus facilisi laoreet, vestibulum erat porta. Dictumst congue gravida maximus porttitor curabitur ad enim mattis. Dui sed blandit erat libero; varius accumsan nostra sem. Ante sagittis orci felis est dignissim suspendisse cras vehicula. Netus curabitur tellus nam consectetur sociosqu. Vulputate vel proin nisi morbi interdum. Dictum ipsum vulputate gravida amet justo orci dictum. Nec rutrum fermentum habitant quis urna; erat cubilia. Natoque fames suspendisse sociosqu morbi placerat rhoncus. Hendrerit erat convallis proin tempus a. Tortor libero dis cubilia tristique diam nam lacinia mattis. Ridiculus ullamcorper urna a suspendisse ultrices egestas ulla"

function addButton(){
  
  const button = document.createElement('button');
  button.textContent = "Summarize";
  
  button.classList.add('summary-button')
  const hoverEffect = document.createElement('div');
  hoverEffect.style.zIndex = '1000';
  hoverEffect.className = 'summary-button__hoverEffect';
  const innerDiv = document.createElement('div');
  innerDiv.style.zIndex = '1000';
  hoverEffect.appendChild(innerDiv);
  button.appendChild(hoverEffect);

  
  
  button.onclick = () => {
    addSummaryCard();
    button.style.display = 'none';
  };

  document.body.appendChild(button);
}

addButton()


// Function to add a card component with sample text
function addSummaryCard() {
  const card = document.createElement('div');
  card.className="summary-card"

  const cardHeader=document.createElement('div')
  const cardTitle=document.createElement('h1')
  cardTitle.textContent="Summary"
  cardHeader.appendChild(cardTitle)
  card.appendChild(cardHeader)
  const cardText = document.createElement('p');
  cardText.textContent = sampleText;
  card.appendChild(cardText);
  document.body.appendChild(card);

  const toggleButton = document.createElement('button');
  toggleButton.textContent = "Toggle";
  toggleButton.classList.add('summary-button');
  let isVisible = true; 

  toggleButton.onclick = () => {
    if (isVisible) {
      card.style.transform = 'translateX(100%)'; 
    } else {
      card.style.transform = 'translateX(0)'; 
    }
    isVisible = !isVisible; 
  };

  document.body.appendChild(toggleButton);

}

