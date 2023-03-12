
let score = 0
let seen_words = []
let time = 60
let canPlay = true

$('#submit').on('click', submitWord);

async function submitWord(evt){
	evt.preventDefault()
	if (!canPlay){return}
	const word = $('input').val();
	
	if (seen_words.includes(word)){
		$('#alert-container').append(`<div id="alert" class="alert alert-info" role="alert">"${word}" has already been played</div>`).css('display', 'block')
			setTimeout(function(){
				$('#alert').remove()
			}, 500)
		$('input').val('')
		return
	} else{
		seen_words.push(word)
	}
	const response = await axios.post('/check', { params: {'word' : word}})
	const result = response.data.result
	show_result(result, word)
	$('input').val('')
}

function show_result(result, word){
	if(result === 'ok'){
		word_len = word.length
		if(word_len < 2){
			$('#alert-container').append(`<div id="alert" class="alert alert-success" role="alert">${word_len} POINT</div>`).css('display', 'block')
			setTimeout(function(){
				$('#alert').remove()
			}, 300)
		}
		else {
			$('#alert-container').append(`<div id="alert" class="alert alert-success" role="alert">${word_len} POINTS</div>`).css('display', 'block')
			setTimeout(function(){
				$('#alert').remove()
			}, 300)
		}
		cal_score(word)
	}
	else if(result === 'not-on-board'){
		$('#alert-container').append(`<div id="alert" class="alert alert-danger" role="alert">"${word}" not on board</div>`).css('display', 'block')
			setTimeout(function(){
				$('#alert').remove()
			}, 500)
	}
	else if(result === 'not-word'){
		$('#alert-container').append(`<div id="alert" class="alert alert-warning" role="alert">"${word}" is not a word</div>`).css('display', 'block')
			setTimeout(function(){
				$('#alert').remove()
			}, 500)
	}
}

function cal_score(word){
	const word_score = word.length
	score += word_score
	$('#score').html(`SCORE: ${score}`)
}

const intervalID = setInterval(timer, 1000)

function timer(){
	time -= 1
	$('#timer').html(`TIME: ${time}secs`)
	if(time === 0){
		canPlay = false
		clearInterval(intervalID)
		send_score(score)
	}
}

async function send_score(score){
	const response = await axios.post('/score', { params: {'new_score' : score}})
	console.log(response)
	const highScore = response.data.high_score
	const numOfPlays = response.data.num_plays
	$('#num-plays').html(`GAME#: ${numOfPlays}`)
	$('#high-score').html(`HIGHSCORE: ${highScore}`)
}