class AdminSetup {

  /**
   * Setup global data
   */
  constructor() {

    // Get current page
    this.currentPage = document.querySelector('h1').textContent.toLowerCase().trim()
    console.log(this.currentPage)
    
    // Globals css selectors
    this.selectors = {
      "image": '.field-image a'
    }

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
      "google_maps_src",
    ]
    let textAreasSelector = 'div > textarea'
    textAreasSelector = noMarkdownIds.map(id => `${textAreasSelector}:not(#id_${id})`).join(", ")
    console.log(textAreasSelector)
    const textAreas = document.querySelectorAll(textAreasSelector)

    setTimeout(() => {
      textAreas.forEach(textArea => {


        var simplemde = new SimpleMDE({
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
   */
  renderImages() {
    const images = document.querySelectorAll(this.selectors.image)
    images.forEach(imageWrapper => {
      this.#renderBaseImage(imageWrapper, "rendered-image")
    })
  }

  /**
   * Run the functions for the current page
   */
  autorun() {
    // Methods to run for each page
    const methods = {
      "propiedades": [this.loadMarkDown],
      "imágenes": [this.renderImages],
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