function myFunction() {
    var checkBox = document.getElementsByName("slider_box");
    for(let i = 0; i < checkBox.length; i++){
      if(checkBox[i].checked){
        console.log(checkBox[i].value);
      }
    }
  }