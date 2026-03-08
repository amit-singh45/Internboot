// Heart animation for like action
function showHeart(event) {
  const btn = event.target.closest('.like-btn');
  const rect = btn.getBoundingClientRect();
  const heart = document.createElement('div');
  heart.classList.add('heart');
  heart.innerHTML = '❤️';
  heart.style.left = (rect.left + rect.width / 2) + 'px';
  heart.style.top = (rect.top + rect.height / 2) + 'px';
  document.body.appendChild(heart);
  setTimeout(() => heart.remove(), 800);
}

document.addEventListener('click', function(e){
  if(e.target.matches('.like-btn')){
    const btn = e.target;
    const postId = btn.dataset.postId;
    const csrftoken = getCookie('csrftoken');
    
    // Show heart animation if liking
    if(!btn.classList.contains('liked')) {
      showHeart(e);
    }
    
    fetch('/like-toggle/', {
      method: 'POST',
      headers: {'X-CSRFToken': csrftoken, 'Content-Type': 'application/x-www-form-urlencoded'},
      body: new URLSearchParams({'post_id': postId})
    }).then(r=>r.json()).then(data=>{
      if(data.action === 'liked') btn.classList.add('liked'); else btn.classList.remove('liked');
      btn.querySelector('.like-count').textContent = data.like_count;
    });
  }

  if(e.target.matches('.follow-btn')){
    const btn = e.target;
    const userId = btn.dataset.userId;
    const csrftoken = getCookie('csrftoken');
    fetch('/follow-toggle/',{
      method:'POST',
      headers: {'X-CSRFToken': csrftoken, 'Content-Type': 'application/x-www-form-urlencoded'},
      body: new URLSearchParams({'user_id': userId})
    }).then(r=>r.json()).then(data=>{
      btn.textContent = data.action === 'followed' ? 'Unfollow' : 'Follow';
    });
  }

  // Dark mode toggle
  if(e.target.matches('#darkModeToggle')){
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
  }
});

function getCookie(name){
  let cookieValue = null;
  if (document.cookie && document.cookie !== ''){
    const cookies = document.cookie.split(';');
    for (let i=0;i<cookies.length;i++){
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name+'=')){
        cookieValue = decodeURIComponent(cookie.substring(name.length+1));
        break;
      }
    }
  }
  return cookieValue;
}

// Initialize dark mode from localStorage
if(localStorage.getItem('darkMode') === 'true'){
  document.body.classList.add('dark-mode');
}

