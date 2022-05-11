import { cookie } from "./cookies.js";

//TO-DO:add history support
class searchList {

    constructor(base) {

        this.base = base;
        this.addresses = {
            "popular": ".searchPromote",
            "result": ".searchResult",
            "history": ".searchHistory"

        }

        this.visibility = {
            "popular": ".searchPromoteBar",
            "result": ".searchResultbar",
            "history": ".searchHistoryBar"
        }


        this.getTable = () => { return document.getElementById(this.tableName) }
        this.getBase = () => { return document.getElementById(this.base) }
        this.tableName = this.getBase().dataset.search;
        this.cookies = new cookie();
        this.cookieName = "hist" + this.tableName;



        this.fetchHandlers = {

            "popular": [{}, 1],
            "result": [{}, 1],
            "history": [{}, 1]
        }

        //this.render();

    }


    resultRender(e, data) {

        this.fetchHandlers["result"][0] = data;

        if (e.currentTarget.value.length == 0) {

            this.zeroType();

        } else {

            this.someType();
            let val = this.getBase().value;

            this.reRender();
            this.someType();
            this.getBase().value = val;
            this.getBase().focus();
            this.getTable().classList.remove("searchHidden");

        }
    }


    render() {


        this.fetchHandlers["history"][0] = this.addHistory()

        this.insertBase();
        this.positionIt();
        this.staticAdd();
        this.handlers();

    }

    reRender() {

        this.getTable().remove();

        this.render();
    }


    cookieAdd(data) {

        let previous = this.cookies.getCookie(this.cookieName);


        if (previous != null) {

            previous = JSON.parse(previous);


        } else {

            previous = {};
        }

        previous = JSON.stringify({...previous, ...data });

        this.cookies.setCookie(this.cookieName, previous);


    }

    removeSingleHistory(key) {

        let previous = JSON.parse(this.cookies.getCookie(this.cookieName));
        delete previous[key]
        this.cookies.setCookie(this.cookieName, JSON.stringify(previous));
        this.reRender();
        this.getTable().classList.toggle("searchHidden");

    }

    removeAllHistory() {

        this.cookies.setCookie(this.cookieName, "{}");
        this.reRender();
        this.getTable().classList.toggle("searchHidden");


    }

    addHistory() {

        let hist = this.cookies.getCookie(this.cookieName);

        this.fetchHandlers["history"][2] = 1;


        if (hist == null) {

            this.fetchHandlers["history"][2] = 0;
            hist = "{}";

        }

        return JSON.parse(hist);

    }



    handlers() {

        //resizeHandler
        window.onresize = () => {

            this.positionIt();

        }


        //queryClick

        document.querySelector(`#${this.tableName} .clearAllHistory`).addEventListener("click", () => {


            this.removeAllHistory();

        })


        document.querySelectorAll(`#${this.tableName}>li>ul>li>a`).forEach((e) => {

            e.addEventListener("click", (e) => {


                if (e.target.textContent.includes("🞭")) {

                    this.removeSingleHistory(e.target.parentElement.textContent.replace("🞭", ""));

                } else {

                    let data = {
                        [e.currentTarget.textContent.replace("🞭", "")]: e.currentTarget.href
                    };

                    this.cookieAdd(data);
                    this.reRender();


                }

            });

        })







        document.addEventListener("click", (e) => {

            console.log(document.activeElement !== this.getBase(), !this.getTable().classList.contains("searchHidden"), !e.target.textContent.includes("🞭"), !e.target.classList.contains("clearAllHistory"));

            if (document.activeElement !== this.getBase() && !this.getTable().classList.contains("searchHidden") && !e.target.textContent.includes("🞭") && !e.target.classList.contains("clearAllHistory")) {

                this.getTable().classList.add("searchHidden");

            }


        })




        this.getBase().addEventListener("focusin", (e) => {


            this.getTable().classList.remove("searchHidden");

        });


        /* 
                this.getBase().addEventListener("keyup", (e) => {


                    if (e.currentTarget.value.length == 0) {

                        this.zeroType();

                    } else {

                        this.someType();
                        let val = this.getBase().value;

                        this.reRender();
                        this.someType();
                        this.getBase().value = val;
                        this.getBase().focus();
                        this.getTable().classList.remove("searchHidden");

                    }

                }); */

    }

    someType() {

        this.removeVisibility("result");
        this.addVisibility("history");

    }

    zeroType() {

        this.addVisibility("result");
        this.removeVisibility("history");

    }


    addVisibility(section) {


        let toggleObj = document.querySelectorAll(`#${this.tableName} ${this.visibility[section]}`);



        for (let index = 0; index < toggleObj.length; index++) {

            toggleObj[index].classList.add("searchHidden");

        }

    }


    removeVisibility(section) {


        let toggleObj = document.querySelectorAll(`#${this.tableName} ${this.visibility[section]}`);



        for (let index = 0; index < toggleObj.length; index++) {

            toggleObj[index].classList.remove("searchHidden");

        }

    }


    add(section, searchParams) {

        this.fetchHandlers[section] = searchParams;



    }




    staticAdd() {

        for (const section in this.fetchHandlers) {


            let searchObj = this.fetchHandlers[section][0],
                count = Object.keys(searchObj).length;

            console.log(section, count)


            if (this.fetchHandlers[section][1] == 1 && count > 0) {

                let code = "";

                for (const key in searchObj) {

                    if (section == "history") {

                        code += `<li class="updateOnKey"><a href=${searchObj[key]}><code class="histCross">&#128941;</code><span>${key}</span></a></li>`;

                    } else {


                        code += `<li class="updateOnKey"><a href=${searchObj[key]}><span>${key}</span></a></li>`;
                    }


                }

                if (section == "result") {

                    document.querySelector(`#${this.tableName} .searchCount`).innerHTML = Object.keys(searchObj).length;

                }


                document.querySelector(`#${this.tableName} ${this.addresses[section]}`).innerHTML += code;


            } else {

                document.querySelectorAll(`#${this.tableName} ${this.visibility[section]}`).forEach((e) => {

                    e.classList.add("mustHide")
                });
            }

        }

        let code = ``;



    }

    insertBase() {

        let codeBase = `
    <div id="psElem">
        
        <ul class="searchTable searchHidden" id="${this.tableName}">

            <li class="searchResultbar searchHidden">
                <div>
                    <span> Found <span class="searchCount"> {result} </span> result </span>
                </div>
            </li>

            <li class="searchResultbar searchHidden">

                <ul class="searchResult">


                </ul>

            </li>



            <li class="searchHistoryBar">
                <div>
                    <span> Recent History </span>
                    <span class="spanButton clearAllHistory"> Clear History </span>
                </div>
            </li>


            <li class="searchHistoryBar">
                <ul class="searchHistory">


                </ul>
            </li>

            <li class="searchPromoteBar">
                <div>
                    <div> Popular Searches </div>
                </div>
            </li>

            <li class="searchPromoteBar">
                <ul class="searchPromote">


                </ul>
            </li>

            </ul>
            
        <div>`;


        document.getElementsByTagName("body")[0].innerHTML += codeBase;

    }

    positionIt() {

        let inputTable = this.getTable(),
            bound = this.getBase().getBoundingClientRect(),
            base = this.getBase()

        inputTable.style.position = "fixed";
        inputTable.style.top = bound.bottom + "px";
        inputTable.style.left = bound.left + "px";
        inputTable.style.width = bound.right - bound.left + "px";
        inputTable.style.height = "auto";
        inputTable.style.maxHeight = window.innerHeight - ((bound.top + base.height) + ((10 * window.innerHeight) / 100)) + "px";


    }



}


var inputSearch = 1;


window.onload = () => {

    inputSearch = new searchList("searchDb");
    inputSearch.add("popular", [{ hello: "#", good: "#" }, 1]);
    inputSearch.add("result", [{ hello: "#", good: "#" }, 1]);
    //inputSearch.add("history", [() => { return { hello: "#" } }, 1]);
    //   inputSearch.add("result", [() => { return { hello: 1 } }, 1]);
    inputSearch.render();


}