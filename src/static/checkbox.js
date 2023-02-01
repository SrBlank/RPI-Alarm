function myFunction() {
    var checkBox = document.getElementsByName("slider_box");
    let checkBox_checked = [];
    let checkBox_unchecked = [];

    for(let i = 0; i < checkBox.length; i++){
      if(checkBox[i].checked){
        checkBox_checked.push(checkBox[i].value);
      } else {
        checkBox_unchecked.push(checkBox[i].value);
      }
    }
    var checkBox_json = {
      "checked" :
        checkBox_checked
      ,
      "unchecked" : 
        checkBox_unchecked      
    }
    
    fetch("/store_data", {
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(checkBox_json),
    })
    .then((response) => response.json())
    .then((data) => {
      console.log('Success:', data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

