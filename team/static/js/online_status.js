const online_status = new WebSocket(
    'ws://'+window.location.host+'/ws/team/online/'
)

online_status.onopen = function(e){
    console.log('conected to online consumer')

}

online_status.onclose = function(e){
    console.log('disconected from online consumer')
}

online_status.onerror = function(e){
    console.log('ERROR')
}
