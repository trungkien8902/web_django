var vUpdateBtn = document.getElementsByClassName('update-cart')

for (i = 0; i < vUpdateBtn.length; i++) {
    vUpdateBtn[i].addEventListener('click', function() {
        var productId = this.dataset.product
        console.log(productId)
        var action = this.dataset.action
        console.log('productId', productId, 'action', action)
        console.log('user', user)
        if (user === 'AnonymousUser') {
            alert('bạn chưa đăng nhập')
        } else {
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action) {
    var url = '/update_item/'
    fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ 'productId': productId, 'action': action })
        })
        .then((response) => {
            return response.json
        })
        .then((data) => {
            location.reload()
        })
}