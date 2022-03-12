let like_button = document.getElementById('like-button');
let like_image = document.getElementById('disactive-like-1');
let like_1_count = document.getElementById('like_count-1');


like_button.addEventListener('click', () => {
    if(like_image.src.includes("likebefore")){
        like_image.src = like_image.src.replace("likebefore", "likeafter");
        // like_image.classList.add("popup-image");
        like_image.style.animation = "popup-image 0.2s ease-in 1 forwards";

        like_1_count.innerText = String(Number(like_1_count.innerText)+1)
    }else{
        like_image.src = like_image.src.replace("likeafter", "likebefore");
        like_image.style.animation = "";
        
        like_1_count.innerText = String(Number(like_1_count.innerText)-1)


    } 
})
try{
    fetch("http://127.0.0.1:8000/", {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
        },
        body:JSON.stringify({name:'krishnan'})
    }).then(() => {alert("Sent Request")})

} catch (err) {
    console.log(err)
}