async function speak() {
  var text = document.getElementById("text").value;
  try {
    var url = "http://localhost:8000/tts?text=" + encodeURIComponent(text);
    var audio = document.getElementById("audio");
    audio.src = url;
    audio.play();
  } catch (error) {
    console.error("Error during fetch or audio playback:", error);
  }
}

document.addEventListener("DOMContentLoaded", (event) => {
  document.getElementById("text").value = "This is a text to speech demo text";
  document.getElementById("speakButton").addEventListener("click", speak);

  fetchVoices();
});
