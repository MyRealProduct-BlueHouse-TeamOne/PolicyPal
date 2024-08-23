// const link = document.createElement('link');
// link.href = chrome.runtime.getURL('../styles.css');
// link.rel = 'stylesheet';
// document.head.appendChild(link);

// const bodyText=document.body.innerText;

// //const summarizedText=await summarize(bodyText)
// const sampleText="Lorem ipsum odor amet, consectetuer adipiscing elit. Velit a nunc per ultrices ac facilisi in semper. Lacinia malesuada ac magna neque adipiscing aenean gravida? Pharetra donec lacus, laoreet erat donec finibus consectetur. Lectus malesuada semper tristique amet aenean taciti lorem diam. Vitae vehicula tempus donec pharetra pulvinar diam quis faucibus. Lacinia fames vel mattis consectetur risus. Senectus justo faucibus ad facilisis proin eleifend. Vitae urna nascetur turpis turpis parturient feugiat nam. Tempus justo efficitur enim duis mauris auctor tellus eu. Platea arcu pharetra pulvinar vestibulum montes dapibus diam. Ante luctus blandit sagittis elit commodo nulla felis. Pellentesque ornare mus habitant felis tempus. Ligula class turpis et consequat nam. Consequat tellus consectetur penatibus semper nulla lectus. Aptent dictum sodales proin fusce egestas congue ridiculus tortor ex. Etiam imperdiet ex suspendisse neque non ornare mus facilisis. Bibendum efficitur augue, lobortis lobortis iaculis urna tortor. Phasellus eros id ut ut suspendisse. Aliquam interdum ut vitae aptent vitae etiam. Bibendum fusce feugiat fringilla arcu consequat ornare habitasse. Purus natoque quis commodo; penatibus donec potenti. Tempus fusce duis metus fusce enim justo nascetur tellus eleifend. Ultrices cras convallis sit ultricies aenean nec luctus. Lectus ultricies et viverra conubia, quam nostra sodales conubia. Conubia eros nascetur et, libero ridiculus id nec consequat. Ornare mollis sollicitudin bibendum luctus facilisi laoreet, vestibulum erat porta. Dictumst congue gravida maximus porttitor curabitur ad enim mattis. Dui sed blandit erat libero; varius accumsan nostra sem. Ante sagittis orci felis est dignissim suspendisse cras vehicula. Netus curabitur tellus nam consectetur sociosqu. Vulputate vel proin nisi morbi interdum. Dictum ipsum vulputate gravida amet justo orci dictum. Nec rutrum fermentum habitant quis urna; erat cubilia. Natoque fames suspendisse sociosqu morbi placerat rhoncus. Hendrerit erat convallis proin tempus a. Tortor libero dis cubilia tristique diam nam lacinia mattis. Ridiculus ullamcorper urna a suspendisse ultrices egestas ulla"


// let isVisible = false;
// let wrapper, toggleButton, card;

// /**
//  * Creates a DOM element with optional class name and text content.
//  * @param {string} type - The type of the element (e.g., 'div', 'p').
//  * @param {string} [className] - The class name to be added to the element.
//  * @param {string} [textContent] - The text content to be set for the element.
//  * @returns {HTMLElement} The created DOM element.
//  */
// function createElement(type, className, textContent) {
//   const element = document.createElement(type);
//   if (className) element.className = className;
//   if (textContent) element.textContent = textContent;
//   return element;
// }

// /**
//  * Sets up the toggle button with click event listener.
//  * @returns {HTMLElement} The toggle button element.
//  */
// function setupToggleButton() {
//   toggleButton = createElement('div', 'toggle-button');
//   toggleButton.addEventListener('click', toggleSummaryCard); // Attach click event listener
//   return toggleButton;
// }

// /**
//  * Sets up the summary card with header and text content.
//  * @returns {HTMLElement} The summary card element.
//  */
// function setupCard() {
//   card = createElement('div', 'summary-card');

//   const cardHeader = createElement('div');
//   const cardTitle = createElement('h1', null, 'Summary');
//   cardHeader.appendChild(cardTitle);
//   card.appendChild(cardHeader);

//   const cardText = createElement('p', null, bodyText);
//   card.appendChild(cardText);

//   return card;
// }

// /**
//  * Adds the summary card and toggle button to the document.
//  */
// function addSummaryCard() {
//   wrapper = createElement('div', 'summary-card__wrapper');
//   wrapper.appendChild(setupToggleButton());
//   wrapper.appendChild(setupCard());

//   document.body.appendChild(wrapper);
// }

// /**
//  * Toggles the visibility of the summary card.
//  */
// function toggleSummaryCard() {
//   if (isVisible) {
//     // Slide out the card
//     wrapper.style.transform = 'translateX(95%)';
//   } else {
//     // Slide in the card
//     wrapper.style.transform = 'translateX(0)';
//   }
//   isVisible = !isVisible;
// }

// // Listen for messages from the Chrome extension
// chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
//   if (request.action === 'showSummaryCard' && !wrapper) {
//     console.log("hooray");
//     addSummaryCard();
//   }
// });

// Revised code
const link = document.createElement('link');
link.href = chrome.runtime.getURL('../styles.css');
link.rel = 'stylesheet';
document.head.appendChild(link);

let isVisible = false;
let wrapper, toggleButton, card;

/**
 * Creates a DOM element with optional class name and text content.
 * @param {string} type - The type of the element (e.g., 'div', 'p').
 * @param {string} [className] - The class name to be added to the element.
 * @param {string} [textContent] - The text content to be set for the element.
 * @returns {HTMLElement} The created DOM element.
 */
function createElement(type, className, textContent) {
  const element = document.createElement(type);
  if (className) element.className = className;
  if (textContent) element.textContent = textContent;
  return element;
}

/**
 * Sets up the toggle button with click event listener.
 * @returns {HTMLElement} The toggle button element.
 */
function setupToggleButton() {
  toggleButton = createElement('div', 'toggle-button');
  toggleButton.addEventListener('click', toggleSummaryCard); // Attach click event listener
  return toggleButton;
}

/**
 * Sets up the summary card with header and text content.
 * @param {string} summaryText - The summary text to be displayed in the card.
 * @returns {HTMLElement} The summary card element.
 */
function setupCard(summaryText) {
  card = createElement('div', 'summary-card');

  const cardHeader = createElement('div');
  const cardTitle = createElement('h1', null, 'Summary');
  cardHeader.appendChild(cardTitle);
  card.appendChild(cardHeader);

  const summaryArray = summaryText.split("\n");

  for (let point = 0; point < summaryArray.length; point++)
  {
    const cardText = createElement('p', null, summaryArray[point]);
    card.appendChild(cardText);
  }

  return card;
}

/**
 * Adds the summary card and toggle button to the document.
 * @param {string} summaryText - The summary text to be displayed in the card.
 */
function addSummaryCard(summaryText) {
  wrapper = createElement('div', 'summary-card__wrapper');
  wrapper.appendChild(setupToggleButton());
  wrapper.appendChild(setupCard(summaryText));

  document.body.appendChild(wrapper);
}

/**
 * Toggles the visibility of the summary card.
 */
function toggleSummaryCard() {
  if (isVisible) {
    // Slide out the card
    wrapper.style.transform = 'translateX(95%)';
  } else {
    // Slide in the card
    wrapper.style.transform = 'translateX(0)';
  }
  isVisible = !isVisible;
}

// Listen for messages from the Chrome extension
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'showSummaryCard' && !wrapper) {
    // Display the summary received from the popup.js script
    console.log("Received summary. Displaying summary card...");
    addSummaryCard(request.summary);
  }
});
