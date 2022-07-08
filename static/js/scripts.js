
if (localStorage.getItem("count") === null){
    localStorage.setItem("count", 1)

}else{
    if (localStorage.getItem("count") % 2 === 0){
        ball.style.transform = "translateX(30px)"
        document.querySelector(".navbar").style.backgroundColor = "black";
        document.querySelector(".navbar").style.color = "white";
        document.body.style.backgroundColor = "black";
        document.body.style.color = "white";
    }else{
        ball.style.transform = "translateX(0px)"
        document.querySelector(".navbar").style.backgroundColor = "#f6f6f6";
        document.querySelector(".navbar").style.color = "black";
        document.body.style.backgroundColor = "white";
        document.body.style.color = "black";
    }
}
document.addEventListener("DOMContentLoaded", function(){
    document.querySelector("#ball").onclick = () => {
        let count = localStorage.getItem("count")
        count++
        if (count % 2 === 0){
            ball.style.transform = "translateX(30px)"
            document.querySelector(".navbar").style.backgroundColor = "black";
            document.querySelector(".navbar").style.color = "white";
            document.body.style.backgroundColor = "black";
            document.body.style.color = "white";
        }else{
            ball.style.transform = "translateX(0px)"
            document.querySelector(".navbar").style.backgroundColor = "#f6f6f6";
            document.querySelector(".navbar").style.color = "black";
            document.body.style.backgroundColor = "white";
            document.body.style.color = "black";
        }
        localStorage.setItem("count", count)
    }
    
})


