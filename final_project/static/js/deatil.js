function getTagClass(tag) {
  if (tag === 'Flagged') {
    return 'bg-danger text-white';
  }
  if (tag === 'Misclassified') {
    return 'bg-warning text-dark';
  }
  if (tag === 'Resolved') {
    return 'bg-success text-white';
  }
  return 'bg-secondary text-white';
}

function renderComment(comment) {
  const tagHtml = comment.tag
    ? `<span class="badge ${getTagClass(comment.tag)} ms-1" style="font-size:0.72rem;">${comment.tag}</span>`
    : '';

  return `
    <div class="comment-block">
      <span class="comment-author">${comment.author}</span>
      <span class="comment-time">${comment.time}</span>
      ${tagHtml}
      <div class="comment-body">${comment.body}</div>
    </div>
  `;
}

async function loadComments() {
  try {
    const response = await fetch(`/api/articles/${ARTICLE_ID}/comments`);
    const comments = await response.json();

    if (!response.ok) {
      alert('Failed to load comments.');
      return;
    }

    const list = document.getElementById('comment-list');
    const count = document.getElementById('comment-count');

    list.innerHTML = '';

    comments.forEach(comment => {
      list.innerHTML += renderComment(comment);
    });

    count.textContent = comments.length;
  } catch (error) {
    console.error(error);
    alert('Something went wrong while loading comments.');
  }
}

async function submitComment() {
  const body = document.getElementById('new-comment').value.trim();
  const tag = document.getElementById('comment-tag').value;

  if (!body) {
    alert('Please enter a comment before posting.');
    return;
  }

  try {
    const response = await fetch(`/api/articles/${ARTICLE_ID}/comments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ body, tag })
    });

    const data = await response.json();

    if (!response.ok) {
      alert(data.error || 'Failed to post comment.');
      return;
    }

    document.getElementById('new-comment').value = '';
    document.getElementById('comment-tag').value = '';

    await loadComments();
  } catch (error) {
    console.error(error);
    alert('Something went wrong while posting the comment.');
  }
}

document.addEventListener('DOMContentLoaded', loadComments);