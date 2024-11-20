document.addEventListener("DOMContentLoaded", () => {
    const images = document.querySelectorAll("div[data-type='horizontal'] img.image-type");
    images.forEach(image => {
      const imageUrl = image.src;
  
      chrome.runtime.sendMessage({ action: "classifyImage", imageUrl }, response => {
        const category = response.category;
        const selectBox = findRelatedSelectBox(image);
        if (selectBox) {
          selectBox.value = category;
          const event = new Event("change");
          selectBox.dispatchEvent(event);
        }
      });
    });
  });
  
  function findRelatedSelectBox(imageElement) {
    // 이미지와 관련된 select box를 찾는 로직
    return imageElement.closest("div")
                        .querySelector("select.form-control.input-sm[name='propertyImageCategory']");
  }
  