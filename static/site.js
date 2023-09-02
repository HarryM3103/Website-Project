var page_loaded = false; //Global variable determining if the page has already been loaded with content

//Function that sends the user's search field data to the backend to be processed
function send_data() {
  document.querySelector(".searchContainer").style.position = "absolute"; //Sets the search box's position to 'absolute'
  document.querySelector(".searchContainer").style.top = "10%"; //Moves the search box to the top of the page
  document.querySelector(".searchContainer").style.transition = "0.5s"; //Adds a transition animation to the search box being moved to the top of the page
  if (page_loaded == true) {
    document.querySelector(".loader").style.visibility = "visible";
  } else {
    setTimeout(function () {
      document.querySelector(".loader").style.visibility = "visible";
    }, 500);
  }

  var item_type = document.getElementById("item_type").value;
  $.ajax({
    url: "/data_received",
    type: "POST",
    data: { name: item_type },
    // After the ajax 'POST' call is finished, call the ajax 'GET' function
  }).done(function () {
    receive_data();
    document.getElementById("item_type").value = "";
    document.querySelector(".itemHolder").innerHTML = "";
  });
}

function receive_data() {
  $.ajax({
    url: "/data_sent",
    method: "GET",
    success: function (result) {
      parse_data(result);
    },
  });
}

function parse_data(data) {
  const items = document.querySelector(".itemHolder");
  for (let i = 0; i < data.length; i += 1) {
    if (items.innerHTML != "") {
      document.querySelector(".loader").style.visibility = "hidden";
    }
    // document.documentElement.style.setProperty('--rating', rating)
    let code = `\
        <div class="card">
            <a href="${data[i][2]}">
            <img src="${data[i][0]}" alt="">
                <div class="cardText">
                    <h2 class="brandText">${data[i][1]}</h2>
                    <p class="itemName">${data[i][3]}</p>
                    <h3 class="itemPrice">$${data[i][4]}</h3>
                    <h5 class="savingPercentage">${data[i][6]}% OFF!</h5>
                    <div class="rating">
                        <h5 class=rating_num>${data[i][8]} <i class="fa-solid fa-star"></i> </h5>
                    </div>  
                    <h6 class="numRatings">${data[i][9]} ratings</h6>
                </div>
            </a>   
        </div>
        `;
    items.innerHTML += code;
  }
  page_loaded = true;
}
