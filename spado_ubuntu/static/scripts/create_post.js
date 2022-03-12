let tags_container = document.getElementById('store-tags');
let tag_input = document.getElementById('tags');
let tag_container = document.getElementById('tag');
let close_button_url = document.getElementById('close-btn-img').src;
let tags = Array();
let counter = 1;


function DeleteTag(self){
    tags.pop(self.classList[self.classList.length-1]);
    self.remove();
}

function AddTag(){
    // Slugifying the tag name
    let tag_name = String(tag_input.value).replace(" ", "-");
    if ((tag_name.length > 2) &&  !(tags.includes(tag_name))) tags.push(tag_name);
    // alert(counter);

    let tag = document.createElement('div');
    tag.id = "tag";
    tags.className = tag_name;
    let tag_text = document.createElement('h4');
    tag_text.innerText = tag_name;
    let close_button = document.createElement('div');
    close_button.className = "close-btn";
    // close_button.classList.add(tag_name);
    // close_button.onclick = DeleteTag();

    let close_image = document.createElement('img');
    close_image.src = close_button_url;
    // close_image.style.transform = "100%";
    close_button.appendChild(close_image);
    close_button.addEventListener('click', ()=>{DeleteTag(tag)});
    tag.appendChild(tag_text);
    tag.appendChild(close_button);
    

    tags.innerHTML = "";
    for(let i = 0; i < tags.length; i++){
        tags_container.appendChild(tag);
        // tags_container.innerHTML += " " + tags[i]; 
    }
    counter++;
} 
