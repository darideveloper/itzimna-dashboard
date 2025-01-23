class AdminSetup {

  /**
   * Setup global data
   */
  constructor() {
    this.currentPage = document.querySelector('h1').textContent.toLowerCase().trim()
    console.log(this.currentPage)
    this.autorun()
  }

  /**
   * Set the value of a text input field
   * @param {string} inputName - The name of the input field (select)
   * @param {string} inputValue  - The value to set the input field to
   */
  loadMarkDown() {
    const textAreas = document.querySelectorAll('div > textarea')

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
   * Run the functions for the current page
   */
  autorun() {
    // Methods to run for each page
    const methods = {
      "propiedades": [this.loadMarkDown],
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