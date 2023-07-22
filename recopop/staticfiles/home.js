function togglePopup() {
    const popup = document.getElementById('popup');
    popup.style.display = popup.style.display === 'block' ? 'none' : 'block';
  }
  
  function postRecommendation() {
    const trackName = document.querySelector('.track-name').value;
    const caption = document.querySelector('.caption').value;
  
    // Do something with the trackName and caption, e.g., post to a server or display on the page.
    console.log('Track Name:', trackName);
    console.log('Caption:', caption);
  
    // Clear the input fields and hide the popup
    document.querySelector('.track-name').value = '';
    document.querySelector('.caption').value = '';
    togglePopup();
  }
  