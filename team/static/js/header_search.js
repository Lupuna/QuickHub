edit = document.querySelector('.edit_for_search_button');
line = document.querySelector('.search_of_header');
main = document.querySelector('.main');
header_2 = document.querySelector('.header_2');
main.addEventListener('click', ()=>{
	if(edit.classList.contains('opened_1')){
		edit.classList.remove('opened_1');
		edit.classList.add('closed_1');
		line.classList.add('w50');
		line.classList.remove('w300');
	};
});
header_2.addEventListener('click', ()=>{
	if(edit.classList.contains('opened_1')){
		edit.classList.remove('opened_1');
		edit.classList.add('closed_1');
		line.classList.add('w50');
		line.classList.remove('w300');
	};
});
edit.addEventListener('click', ()=>{
	if(edit.classList.contains('closed_1')){
		edit.classList.remove('closed_1');
		edit.classList.add('opened_1');
		line.classList.add('w300');
		line.classList.remove('w50');
	};
});
