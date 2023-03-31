// Hides section1 and shows section2
function showSection(section1, section2) {
    document.querySelector(section1).style.display = "none";
    document.querySelector(section2).style.display = "block";
}

document.addEventListener('DOMContentLoaded', function() {
    // id of the post that's have been clicked for editing (declaration)
    let id;

    // Adds click event listener to every edit button
    document.querySelectorAll('.edit').forEach(function(post) {
        post.addEventListener('click', function() {
            id = this.dataset.id;
            showSection(`#post${id}`, `#editForm${id}`);

            // Edit form's functionality
            const edit = document.querySelector(`#editForm${id}`).querySelector('textarea');
            const submit = document.querySelector(`#editForm${id}`).querySelector('button');

            edit.innerHTML = edit.dataset.content;
            // For getting value of edit form's textarea
            edit.onkeyup = function() {
                if (edit.value.length === 0) {
                    submit.disabled = true;
                } else {
                    submit.disabled = false;
                }
            }            


            document.querySelector(`#editForm${id}`).onsubmit = function() {
                // Changing post on frontend
                let content = edit.value
                document.querySelector(`#post${id}`).querySelector('.post').innerHTML = content;

                // Editing the database
                let url = new Request(
                    `http://127.0.0.1:8000/edit/${id}`,
                    {headers: {'X-CSRFToken': csrftoken}}
                    );
                    
                fetch(url, {
                    method: 'PUT',
                    body: JSON.stringify({
                        content: content
                    }),
                    mode: 'same-origin'
                })

                showSection(`#editForm${id}`, `#post${id}`)

                return false;
            }
        });
    });    
});
