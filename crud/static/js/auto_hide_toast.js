setTimeout(() => {
  const toast = document.getElementById('toast-success');

  if (toast) {
    toast.style.transition = 'opacity 0.5s ease';
    toast.style.opacity = '0';

    setTimeout(() => {
      toast.style.display = 'none';
    }, 500);
  }
}, 3000);