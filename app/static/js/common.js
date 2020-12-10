function copyToClip() {
  var copyText = document.getElementById("wrapped_html");
  copyText.select();
  copyText.setSelectionRange(0, 99999)
  document.execCommand("copy");
  alert(copyText.value)
}