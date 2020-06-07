let updateBtns = document.getElementsByClassName('update-cart')

for(i=0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        let productId = this.dataset.product 
        let action = this.dataset.action 
        console.log("productID:",productId, 'Action:',action)

        // console.log(user)
        if(user === "AnonymousUser") {
            console.log('not logged in')
        }else{
            update_user_order(productId,action)
        }
    })
}

function update_user_order(productId,action){
    console.log("User logged in, sending data...")

    let url = '/update_item/'
    fetch(url, {
        method : "POST",
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken
        },
        body:JSON.stringify({
            "productId":productId,
            "action":action
        })
    })

    .then((response) => {
        return response.json()
    })

    .then ((data) => {
        console.log("data", data)
        location.reload()
    })
}