import { searchList } from "../vendors/search/js/search.js"
import { cookie } from "../vendors/search/js/cookies.js"

var searchTest = "",
    searchPin = "",
    cookies = new cookie();

function getCookie(name) {
    let r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function success1(message) {

    $(".notification").css({ "display": "none" })

    let notification = $("#notificationSuccess");

    notification[0].innerText = message;

    notification.css("display", "flex");

    setTimeout(() => {
        $(".notification").css({ "display": "none" })
    }, 5000);
}

function updateCount(count) {

    $(".cart-count")[0].innerText = count;

}

function sendPost(data, url, cb) {

    /* console.log(url); */

    $.ajax({

        type: "POST",
        url: url,
        data: data,
        success: cb,
        dataType: "text",
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('_xsrf'));
        }
    })

}


function setPrice() {



    if ($('#_11').length == 1) {

        searchPin = new searchList("_11")
        searchPin.href = false;
        searchPin.hPercent = 20;
        searchPin.funcPlug = setPrice;
        //searchPin.add("popular", [{ hello: "#", good: "#" }, 1]);
        searchPin.render();

        let last = searchPin.getLast();

        if (last != null) {
            let lastKey = last,
                data = "",
                url = "",
                cb = "";

            $("#_11").val(last);

            sendPost(data = { "pincode": lastKey }, url = `/areaPrice`, cb = (response) => {

                response = JSON.parse(response);

                if (response["result"]) {


                    $(`#totalPrice`)[0].innerText = "₹" + (parseFloat($("#cost").val()) + parseFloat(response["data"][0]));
                    $(`#totalPriceBar`).css("display", "flex");

                }
            });




        }


    }





}



$(document).ready((e) => {

    //TODO add handler for cart counter update on reload

    let data = {},
        url = {},
        cb = {};

    sendPost(data = { "nature": "count" }, url = "/addToCart", cb = (response) => {

        /* console.log("good"); */

        response = JSON.parse(response);

        if (response["result"]) {

            updateCount(response["data"]["count"]);
        }
    });








    let r = setInterval(() => {

        let t = $("#preloader").css("display");

        if (t == "none") {

            searchTest = new searchList("_1");
            searchTest.add("popular", [{ hello: "#", good: "#" }, 1]);
            searchTest.funcPlug = setPrice;
            //searchTest.add("result", [{ hello: "#", good: "#" }, 1]);
            searchTest.render();


            setPrice()




            clearInterval(r);

            document.getElementById("_1").addEventListener("keyup", (e) => {

                sendPost(data = {}, url = `/search?searchTerm=${e.currentTarget.value}`, cb = (response) => {

                    response = JSON.parse(response);

                    if (response["result"]) {

                        searchTest.resultRender([response["data"], 1]);
                    }
                });



            });






            document.getElementById("_11").addEventListener("keyup", (e) => {


                sendPost(data = { "pincode": e.currentTarget.value }, url = `/area`, cb = (response) => {

                    response = JSON.parse(response);

                    if (response["result"]) {

                        searchPin.resultRender([response["data"], 1]);
                    }
                });



            });






        }

    }, 300);








    //addTOCart Click

    $("body").on("click", ".addToCart", (e) => {

        let id = $(e.currentTarget).attr("data-id"),
            nature = $(e.currentTarget).attr("data-nature"),
            message = id.includes("PACK") ? "Package Added Successfully" : "Test Added Successfully",
            data = {},
            url = {},
            cb = {};




        sendPost(data = { "id": id, "pack": id.includes("PACK"), "nature": nature },
            url = "/addToCart", cb = (response) => {

                response = JSON.parse(response)

                /* console.log(response["result"]); */

                if (response["result"]) {

                    success1(message);

                    updateCount(response["data"]["count"])


                }
            })

    })

})