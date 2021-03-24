$('select').on('change', function() {
    if(window.location.pathname != "/post/new/"){
        sessionStorage.setItem("value",this.value);
        window.location.href = "/posts/day/"+this.value;
    }
  });
