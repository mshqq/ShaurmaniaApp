let phoneMaskInstance = null;

function configPhoneMask() {
  const phoneInput = document.querySelector('#customerPhone');
  if (!phoneInput) return;

  phoneMaskInstance = IMask(phoneInput, {
    mask: `+{7} (000) 000-00-00`
  });
}

function getPhoneMask() {
  return phoneMaskInstance;
}

export default configPhoneMask;
export { getPhoneMask };
