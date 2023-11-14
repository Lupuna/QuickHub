menu_icon = document.querySelector('.button_burger');
text_in_btns = document.getElementsByClassName('text_on_left_menu');
btns = document.getElementsByClassName('left_menu');
btn = document.getElementsByClassName('sub_menu_left');
menu_icon.addEventListener('click', ()=>{
	if(text_in_btns[0].classList.contains('_show')){
		for (let i = 0; i < 5; i++) {
  			text_in_btns[i].classList.remove('_show');
			text_in_btns[i].classList.add('_non_visible');
		}
		btns[0].classList.remove('_w200');
		btns[0].classList.add('_w70');
		btn[0].classList.remove('_w200');
		btn[0].classList.add('_w70');
	}else{
		for (let i = 0; i < 5; i++) {
			text_in_btns[i].classList.remove('_non_visible');
			text_in_btns[i].classList.add('_show');
		}
		btns[0].classList.add('_w200');
		btns[0].classList.remove('_w70');
		btn[0].classList.add('_w200');
		btn[0].classList.remove('_w70');
	}
});