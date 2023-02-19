$("select").on("change", function () {
  if (window.location.pathname != "/post/new/") {
    sessionStorage.setItem("value", this.value);
    window.location.href = "/day/" + this.value;
  }
});

function validateSize(file) {
  let fileSize = file.files[0].size;
  let fileLimit = 5 * 1024 * 1024;
  if (fileSize > fileLimit) {
    alert("Sorry, your file size exceeds 5 MB.");
    $(file).val("");
  }
}

window.onscroll = function () {
  let header = document.getElementById("header");
  if (document.body.scrollTop > 82 || document.documentElement.scrollTop > 82) {
    header.classList.add("header-shrink");
  } else {
    header.classList.remove("header-shrink");
  }
};

window.onload = function () {
  let header = document.getElementById("header");
  if (document.body.scrollTop > 82 || document.documentElement.scrollTop > 82) {
    header.classList.add("header-shrink");
  } else {
    header.classList.remove("header-shrink");
  }
};

