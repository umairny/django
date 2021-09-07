// Comment the user's post the current post
function comm(id) {
        const replyed = document.querySelector('#reply-' + id)
        const comment = document.querySelector('#comment-' + id)
        const reply = document.querySelector('#reply' + id)
        const combtn = document.querySelector('#combtn' + id)
        
        combtn.style.display = 'none';
        comment.style.display = 'block';
        reply.style.display = 'inline-block';

        reply.addEventListener('click', () => {
            fetch('comment/' + id, {
                method: 'PUT',
                body: JSON.stringify({
                    post: comment.value
                })
            })
            comment.style.display = 'none';
            reply.style.display = 'none';
            combtn.style.display = 'none';

            replyed.style.display = 'block';
            replyed.innerHTML  = "comments: " + comment.value;
        })
        //lert('comment')
}

//like and unlike the post
function like(id) {
    const likebtn = document.querySelector(`#like${id}`)
    const total_like = document.querySelector(`#total_like${id}`)
    const liked = document.querySelector(`#liked${id}`)

    fetch('like/'+id, {
        method: 'PUT',
        body: JSON.stringify({liked: "Like", post_id: id})
        })
        .then((res) => res.json())
        .then((res) => {
            console.log(res)
            if (res.status == 201) {
                if (res.liked === "Like") {
                    total_like.innerHTML = res.total_like;
                    liked.innerHTML = res.liked;
                } else if (res.liked === "Liked") {
                    total_like.innerHTML = res.total_like;
                    liked.innerHTML = res.liked;
                }
                
            }
        })
   
}


// Edit the current post
function edit(id) {
        const post = document.querySelector('#post-' + id)
        const edit = document.querySelector('#edit-text-' + id)
        const save = document.querySelector('#save' + id)
        const editBtn = document.querySelector('#edit-btn-' + id)

        editBtn.style.display = 'none';
        post.style.display = 'none';
        edit.style.display = 'block';
        save.style.display = 'inline-block';

        save.addEventListener('click', () => {
            fetch('edit/' + id, {
                method: 'PUT',
                body: JSON.stringify({
                    post: edit.value
                })
            })
            edit.style.display = 'none';
            save.style.display = 'none';

            post.style.display = 'block';
            editBtn.style.display = 'inline-block';
            post.innerHTML = edit.value;
        })
           //alert('hello' + id)
}


