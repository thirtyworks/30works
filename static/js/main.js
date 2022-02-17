$('select').on('change', function() {
    if(window.location.pathname != "/post/new/"){
        sessionStorage.setItem("value",this.value);
        window.location.href = "/posts/day/"+this.value;
    }
  });

function validateSize(file){
    let fileSize = file.files[0].size
    let fileLimit = 5 * 1024 * 1024
    if (fileSize > fileLimit) {
        alert('Sorry, your file size exceeds 5 MB.');
        $(file).val('');
    } 
}
