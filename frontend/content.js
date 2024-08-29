// Create a link element to include the stylesheet for the summary card
const link = document.createElement("link");
link.href = chrome.runtime.getURL("../styles.css"); // Set the href to the stylesheet URL from the Chrome extension
link.rel = "stylesheet"; // Set the rel attribute to stylesheet
document.head.appendChild(link); // Append the link element to the document head

// Initialize variables for tracking visibility and storing DOM elements
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
  const element = document.createElement(type); // Create the element of specified type
  if (className) element.className = className; // Add class name if provided
  if (textContent) element.textContent = textContent; // Set text content if provided
  return element; // Return the created element
}

/**
 * Sets up the toggle button with click event listener.
 * @returns {HTMLElement} The toggle button element.
 */
function setupToggleButton() {
  toggleButton = createElement("div", "toggle-button"); // Create the toggle button with a class name
  toggleButton.addEventListener("click", toggleSummaryCard); // Attach click event listener to toggle the summary card
  return toggleButton; // Return the toggle button element
}

/**
 * Sets up a loading card with shimmer effect elements.
 * @returns {HTMLElement} The loading card element.
 */
function setupLoadingCard() {
  card = createElement("div", "summary-card"); // Create the summary card container

  const cardHeader = createElement("div"); // Create a header for the card
  const cardTitle = createElement("h1", null, "Summary"); // Create a title element with the text 'Summary'
  cardHeader.appendChild(cardTitle); // Append the title to the header
  card.appendChild(cardHeader); // Append the header to the card

  // Add shimmer loading effects to simulate loading state
  for (let i = 0; i < 10; i++) {
    card.appendChild(createElement("div", "shimmerBG")); // Append shimmer background divs
  }

  return card; // Return the loading card element
}

/**
 * Adds text content to the summary card, removing loading animations.
 * @param {string} summaryText - The summary text to be displayed in the card.
 */
function addCardText(summaryText) {
  // Remove loading elements (shimmer effects) from the card
  const blurredBGs = card.querySelectorAll(".shimmerBG");
  console.log(blurredBGs); // Log the removed shimmer elements
  blurredBGs.forEach((blurredBG) => card.removeChild(blurredBG)); // Remove each shimmer element from the card

  // Split the summary text by new lines and add each line as a paragraph
  const summaryArray = summaryText.split("\n");

  for (let point = 0; point < summaryArray.length; point++) {
    const cardText = createElement("p", null, summaryArray[point]); // Create a paragraph for each summary point
    card.appendChild(cardText); // Append the paragraph to the card
  }
  return card; // Return the card with added text
}

/**
 * Adds the summary card and toggle button to the document.
 */
function addSummaryCard() {
  wrapper = createElement("div", "summary-card__wrapper"); // Create a wrapper for the summary card and toggle button
  wrapper.appendChild(setupToggleButton()); // Add the toggle button to the wrapper
  wrapper.appendChild(setupLoadingCard()); // Add the loading card to the wrapper

  document.body.appendChild(wrapper); // Append the wrapper to the document body
}

/**
 * Toggles the visibility of the summary card.
 */
function toggleSummaryCard() {
  if (isVisible) {
    // Slide out the card when it is currently visible
    wrapper.style.transform = "translateX(95%)";
  } else {
    // Slide in the card when it is currently hidden
    wrapper.style.transform = "translateX(0)";
  }
  isVisible = !isVisible; // Toggle the visibility state
}

/**
 * Fetches the summary from the server using the provided terms.
 * @param {string} terms - The terms to summarize.
 * @returns {Promise<string>} The summary text returned from the server.
 */
async function fetchSummary(terms) {
  try {
    // Send a POST request to the server to get the summary
    const response = await fetch("http://localhost:3000/summarize", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ terms }), // Include terms in the request body
    });

    // Check if the response status is OK
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`); // Throw error if response is not ok
    }

    const data = await response.json(); // Parse response JSON data
    return data.summary; // Return the summary from the response
  } catch (error) {
    console.error("Failed to fetch summary:", error.message); // Log any errors encountered
  }
}

// Listen for messages from the Chrome extension
chrome.runtime.onMessage.addListener(async (request, sender, sendResponse) => {
  // Check if the action is to show the summary card and the wrapper is not already created
  if (request.action === "showSummaryCard" && !wrapper) {
    // Display the summary card and fetch the summary from the server
    addSummaryCard();
    const terms = document.body.innerText; // Extract the text from the document body as terms
    const response = await fetchSummary(terms); // Fetch summary for the terms
    console.log(response); // Log the response for debugging
    addCardText(response); // Add the summary text to the card
  }
});
