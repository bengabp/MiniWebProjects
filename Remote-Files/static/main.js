
$(document).ready(()=>{
    let logo_icon =  document.getElementById("logo-icon");
    let floating_footer = document.getElementById("page-footer");
    let panel_up = true;
    let fav_panel_up = false;
    let current_subPage = "all";

    let searchBar = document.getElementById("search-field");
    searchBar.addEventListener("input",onSearchBarInput);

    let favPanel = document.getElementById("page-main-side-favourites");
    let mainPage = document.getElementById("page-main-side-content");

    let displayFavBtn = document.getElementById("display-fav-btn");
    displayFavBtn.addEventListener("click",onDisplayFavBtnClick);
    

    String.prototype.toProperCase = function () {
        return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    };

    logo_icon.addEventListener('click',()=>{
        rect = floating_footer.getBoundingClientRect();
        panel_up = ! panel_up;

        if (panel_up){
            floating_footer.style.bottom = "0px";

        }else {
            floating_footer.style.bottom = "-100px";
        }
    });


    let file_upload_btn = document.getElementById("file-upload");
    file_upload_btn.addEventListener("input",(data)=>{
        let upload_file = data.target.files;
        if (upload_file){
            let formdata = new FormData();
            formdata.append("file",upload_file[0]);

            $.ajax({
                url:"/",
                type:"POST",
                async:false,
                cache:false,
                processData:false,
                contentType:false,
                data:formdata,
                enctype:"multipart/form-data",
                success:(response)=>{
                    if (response.messageCode==1){
                        do_refresh();
                    }
                }
            });
        }
    });

    function do_refresh(q=""){
        $.ajax({
            url:"/get-all-files"+"?q="+q,
            type:"GET",
            success:(data)=>{
                let items_container = document.getElementById("page-main-side-content");
                let current_items = items_container.getElementsByClassName("item");
                
                searchBar.placeholder = "Search All Files . . .";

                $("#page-main-side-content").empty();

                
                if (data.files.length === 0){
                    items_container.innerHTML += `
                    
                    <h1 class="no-files">
                        😞 No Files were Found
                    </h1>

                    `
                } else {
                    let subPageLabel = document.createElement("h1");
                    subPageLabel.textContent = "All Files";
                    subPageLabel.style.margin = "0";
                    subPageLabel.style.marginLeft = "10px";
                    items_container.appendChild(subPageLabel);
                }

                data.files.forEach(new_item =>{
                    let new_element = document.createElement("div");
                    new_element.id = `item-${new_item.unique_hash}`;
                    new_element.classList.add("item");

                    new_element.innerHTML = 
                    `
                        <div class="item-header">
                            <span>${new_item.filename}</span>
                            <span>${new_item.filesize}</span>
                        </div>
                        <div class="item-body">
                            <label>${new_item.extension}</label>
                            <div>
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-clock-fill" viewBox="0 0 16 16">
                                    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/>
                                </svg>
                                <span>${new_item.created_at}</span>
                            </div>
                        </div>
                        <div class="item-footer">
                            <!-- Download Icon -->
                            <a href="/files/${new_item.filename}" download class="button-link">
                                <div class="menu-btn" data-id='download-btn'>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-cloud-arrow-down-fill" viewBox="0 0 16 16">
                                        <path d="M8 2a5.53 5.53 0 0 0-3.594 1.342c-.766.66-1.321 1.52-1.464 2.383C1.266 6.095 0 7.555 0 9.318 0 11.366 1.708 13 3.781 13h8.906C14.502 13 16 11.57 16 9.773c0-1.636-1.242-2.969-2.834-3.194C12.923 3.999 10.69 2 8 2zm2.354 6.854-2 2a.5.5 0 0 1-.708 0l-2-2a.5.5 0 1 1 .708-.708L7.5 9.293V5.5a.5.5 0 0 1 1 0v3.793l1.146-1.147a.5.5 0 0 1 .708.708z"/>
                                    </svg>
                                    <span>Download</span>
                                </div>
                            </a>

                            <div class="menu-btn" data-id='fav-btn'>
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
                                    <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                </svg>
                                <span>Add to Favourites</span>
                            </div>
                            
                            <div class="menu-btn" data-id='delete-btn'>
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                                    <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/>
                                </svg>
                                <span>Delete</span>
                            </div>
                        </div>
                    ` 
                    items_container.append(new_element)
                    new_element.querySelector("[data-id='download-btn']").addEventListener('click',onclickItemButton)
                    new_element.querySelector("[data-id='delete-btn']").addEventListener('click',onclickItemButton)
                    new_element.querySelector("[data-id='fav-btn']").addEventListener('click',onclickItemButton)

                });
                
            },
            error:(error)=>{
                console.log("An Error occurred "+error);
            }
        });

        // Get Favourite files
        $.ajax({
            url:"/favourites/",
            type:"GET",
            success:(data)=>{
                
                let items_container = document.getElementById("page-main-side-favourites");
                let current_fav_items = items_container.getElementsByClassName("item");

                $("#page-main-side-favourites").empty();

                items_container.innerHTML += `
                
                <div id="page-main-side-favourites-header">
                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
                        <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                    </svg>
                    <h1>Favourites</h1>
                </div>

                `

                if (data.results.length === 0){
                    items_container.innerHTML += `
                    
                    <h1 class="no-files">
                     Your Favourite files appear here
                    </h1>

                    `
                }
                
                data.results.forEach(new_item =>{
                    let new_element = document.createElement("div");
                    new_element.id = `item-${new_item.unique_hash}`;
                    new_element.classList.add("item");

                    new_element.innerHTML = 
                    `
                        <div class="item-header">
                            <span>${new_item.filename}</span>
                            <span>${new_item.filesize}</span>
                        </div>
                        <div class="item-body">
                            <label>${new_item.extension}</label>
                            <div>
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-clock-fill" viewBox="0 0 16 16">
                                    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/>
                                </svg>
                                <span>${new_item.created_at}</span>
                            </div>
                        </div>
                        <div class="item-footer">
                            <!-- Download Icon -->
                            <a href="/files/${new_item.filename}" download class="button-link">
                                <div class="menu-btn" data-id='fav-download-btn'>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-cloud-arrow-down-fill" viewBox="0 0 16 16">
                                        <path d="M8 2a5.53 5.53 0 0 0-3.594 1.342c-.766.66-1.321 1.52-1.464 2.383C1.266 6.095 0 7.555 0 9.318 0 11.366 1.708 13 3.781 13h8.906C14.502 13 16 11.57 16 9.773c0-1.636-1.242-2.969-2.834-3.194C12.923 3.999 10.69 2 8 2zm2.354 6.854-2 2a.5.5 0 0 1-.708 0l-2-2a.5.5 0 1 1 .708-.708L7.5 9.293V5.5a.5.5 0 0 1 1 0v3.793l1.146-1.147a.5.5 0 0 1 .708.708z"/>
                                    </svg>
                                    <span>Download</span>
                                </div>
                            </a>
                            
                            <div class="menu-btn" data-id='fav-delete-btn'>
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                                    <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/>
                                </svg>
                                <span>Remove</span>
                            </div>
                        </div>
                    ` 
                    items_container.append(new_element)
                    new_element.querySelector("[data-id='fav-download-btn']").addEventListener('click',onclickItemButton)
                    new_element.querySelector("[data-id='fav-delete-btn']").addEventListener('click',onclickItemButton)

                });
                
            },
            error:(error)=>{
                console.log("An Error occurred "+error);
            }
        });
    }
    // Get all files on server
    do_refresh();

    function onclickItemButton(event){
        let item =  event.currentTarget.parentElement.parentElement;
        let filename = item.querySelector("span").textContent;
        let button = event.currentTarget;
        let dataId = button.attributes.getNamedItem("data-id").value;

        if (dataId === "download-btn"){
            // Implement Download feature
            

        } else if (dataId === "delete-btn"){
            // Implement Delete Feature
            $.ajax({
                url:"/"+filename,
                type:"DELETE",
                async:false,
                cache:false,
                processData:false,
                contentType:false,
                enctype:"multipart/form-data",
                success:(response)=>{
                    if (response.messageCode==1){
                        do_refresh();
                    }
                }
            });
        } else if (dataId === "fav-btn"){
            // Implement Delete Feature for Favourites
            $.ajax({
                url:"/favourites/",
                type:"POST",
                timeout:0,
                headers:{
                    "Content-Type":"application/json"
                },
                data:JSON.stringify({
                    "filename":filename
                }),
                success:(response)=>{
                    do_refresh();
                }
            });
            
        } else if (dataId === "fav-delete-btn"){
            // Implement Delete Feature for Favourites
            $.ajax({
                url:"/favourites/"+filename,
                type:"DELETE",
                async:false,
                cache:false,
                processData:false,
                contentType:false,
                enctype:"multipart/form-data",
                success:(response)=>{
                    do_refresh();
                }
            });
        }
    }

    $(".nav-btn").on("click",(event)=>{
        let clickedButton = event.currentTarget;
        let buttonDataId = clickedButton.attributes.getNamedItem("data-id");
        
        if (buttonDataId.value === "all-files-btn"){
            current_subPage = "all";
            do_refresh();
        } else {
            do_dynamic_refresh(file_type=buttonDataId.value.split('-')[1]);
        }
    });

    function do_dynamic_refresh(file_type){
        current_subPage = file_type
        $.ajax({
            url:"/get-all-files?category="+file_type,
            type:"GET",
            success:(data)=>{
                
                let items_container = document.getElementById("page-main-side-content");
                let current_items = items_container.getElementsByClassName("item");

                $("#page-main-side-content").empty();
                
                
                searchBar.placeholder = `Search ${file_type.toProperCase()} . . .`;
                
                
                if (data.files.length === 0){
                    items_container.innerHTML += `
                    
                    <h1 class="no-files">
                        😞 No Files were Found
                    </h1>

                    `
                } else {
                    let subPageLabel = document.createElement("h1");
                    subPageLabel.textContent = file_type.toProperCase();
                    subPageLabel.style.margin = "0";
                    subPageLabel.style.marginLeft = "10px";
                    items_container.appendChild(subPageLabel);
                }
                
                data.files.forEach(new_item =>{
                    let new_element = document.createElement("div");
                    new_element.id = `item-${new_item.unique_hash}`;
                    new_element.classList.add("item");

                    new_element.innerHTML = 
                    `
                        <div class="item-header">
                            <span>${new_item.filename}</span>
                            <span>${new_item.filesize}</span>
                        </div>
                        <div class="item-body">
                            <label>${new_item.extension}</label>
                            <div>
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-clock-fill" viewBox="0 0 16 16">
                                    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/>
                                </svg>
                                <span>${new_item.created_at}</span>
                            </div>
                        </div>
                        <div class="item-footer">
                            <!-- Download Icon -->
                            <a href="/files/${new_item.filename}" download class="button-link">
                                <div class="menu-btn" data-id='download-btn'>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-cloud-arrow-down-fill" viewBox="0 0 16 16">
                                        <path d="M8 2a5.53 5.53 0 0 0-3.594 1.342c-.766.66-1.321 1.52-1.464 2.383C1.266 6.095 0 7.555 0 9.318 0 11.366 1.708 13 3.781 13h8.906C14.502 13 16 11.57 16 9.773c0-1.636-1.242-2.969-2.834-3.194C12.923 3.999 10.69 2 8 2zm2.354 6.854-2 2a.5.5 0 0 1-.708 0l-2-2a.5.5 0 1 1 .708-.708L7.5 9.293V5.5a.5.5 0 0 1 1 0v3.793l1.146-1.147a.5.5 0 0 1 .708.708z"/>
                                    </svg>
                                    <span>Download</span>
                                </div>
                            </a>

                            <div class="menu-btn" data-id='fav-btn'>
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
                                    <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                                </svg>
                                <span>Add to Favourites</span>
                            </div>
                            
                            <div class="menu-btn" data-id='delete-btn'>
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                                    <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/>
                                </svg>
                                <span>Delete</span>
                            </div>
                        </div>
                    ` 
                    items_container.append(new_element)
                    new_element.querySelector("[data-id='download-btn']").addEventListener('click',onclickItemButton)
                    new_element.querySelector("[data-id='delete-btn']").addEventListener('click',onclickItemButton)
                    new_element.querySelector("[data-id='fav-btn']").addEventListener('click',onclickItemButton)

                });
                
            },
            error:(error)=>{
                console.log("An Error occurred "+error);
            }
        });
    }

    // Live Search Implementation
    function onSearchBarInput(event){
        let searchInput = document.getElementById("search-field");
        let searchText = searchInput.value.trim();
        do_refresh(q=searchText);
    }

    function onDisplayFavBtnClick(event){
        console.log(favPanel);
        fav_panel_up = !fav_panel_up
        if (fav_panel_up){
            mainPage.style.filter = "blur(10px)";
            favPanel.style.transform = "translateY(0%)";
        } else {
            favPanel.style.transform = "translateY(130%)";
            mainPage.style.filter = "blur(0px)";
        }
    }

    window.onresize = (event)=>{
        let winWidth = window.innerWidth;
        if (winWidth > 1000){
            favPanel.style.transform = "translateY(0%)";
            mainPage.style.filter = "blur(0px)";
            fav_panel_up = false;
        } else {
            console.log("HEre",fav_panel_up)
            favPanel.style.transform = "translateY(130%)";
            if (fav_panel_up === false){
                mainPage.style.filter = "blur(0px)";
            } else {
                mainPage.style.filter = "blur(10px)";
            }
        }
    }
 
});
