class AdminSetup {

  /**
   * Setup global data
   */
  constructor() {

    // Get current page
    this.currentPage = document.querySelector('h1').textContent.toLowerCase().trim()
    console.log(this.currentPage)

    // Run methods in each page
    this.autorun()
  }

  /**
 * Load the base image (image, logo, icon, etc) who match with the selector
 * 
 * @param {string} selector - The css selector to find the images
 * @param {string} className - The class name to add to the image
 */
  #renderBaseImage(imageWrapper, className) {
    // Get link
    const link = imageWrapper.href

    // Create image tag
    const imageElem = document.createElement("img")
    imageElem.classList.add(className)
    imageElem.classList.add("rendered-media")
    imageElem.src = link

    // Append element to the wrapper
    imageWrapper.innerHTML = ""
    imageWrapper.appendChild(imageElem)
    imageWrapper.target = "_blank"
  }

  /**
   * Set the value of a text input field
   * @param {string} inputName - The name of the input field (select)
   * @param {string} inputValue  - The value to set the input field to
   */
  loadMarkDown() {

    // Get text areas
    const noMarkdownIds = [
      "google_maps_src", // Property google maps src field
      "description", // Post description field
    ]
    let textAreasSelector = 'div > textarea'
    const notSelector = noMarkdownIds.map(id => `:not(#id_${id})`).join("")
    textAreasSelector = `div > textarea${notSelector}`
    const textAreas = document.querySelectorAll(textAreasSelector)

    setTimeout(() => {
      textAreas.forEach(textArea => {
        new SimpleMDE({
          element: textArea,
          toolbar: [
            "bold", "italic", "heading", "|",
            "quote", "code", "link", "image", "|",
            "unordered-list", "ordered-list", "|",
            "undo", "redo", "|",
            "preview",
          ],
          spellChecker: false,
        })
      })
    }, 100)
  }

  /**
   * Render regular image images
   * 
   * @param {string} selector_images - The css selector to find the images
   */
  renderImages(selector_images) {
    const images = document.querySelectorAll(selector_images)
    images.forEach(imageWrapper => {
      this.#renderBaseImage(imageWrapper, "rendered-image")
    })
  }

  setupCopyButtons() {
    const copyButtons = document.querySelectorAll('.copy-btn')
    console.log(copyButtons)
    copyButtons.forEach(button => {
      button.addEventListener('click', () => {
        const copyAttrib = "value-copy"
        const copyValue = button.getAttribute(copyAttrib)
        const originalText = button.textContent
        button.textContent = "Copiado!"

        // Copy value to clipboard
        navigator.clipboard.writeText(copyValue).then(() => {
          // Show message in button
          button.textContent = "Copiado!"
          setTimeout(() => {
            button.textContent = originalText
          }, 2000)
        }).catch(err => {
          console.error('Error copying text: ', err)
        })
      })
    })
    
  }

  /**
   * Run the functions for the current page
   */
  autorun() {
    // Methods to run for each page
    const methods = {
      "propiedades": [this.loadMarkDown],
      "imágenes": [() => this.renderImages('.field-image a'), this.setupCopyButtons],
      "entradas": [this.loadMarkDown],
      "empresas": [this.loadMarkDown, () => this.renderImages('.field-logo a'), () => this.renderImages('.field-banner a')],
    }

    // Run the methods for the current page
    if (methods[this.currentPage]) {
      for (let method of methods[this.currentPage]) {
        method.call(this)
      }
    }
  }
}

new AdminSetup()