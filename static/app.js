const intervalID = setInterval(timer, 1000)
let time = 60
let score = 0
let seenWords = []
let canPlay = true

$('#submit').on('click', submitWord);

/* sends word to server to evaluate*/
async function submitWord(evt){
	evt.preventDefault()
	if (!canPlay){return}
	const word = ($('input').val()).toLowerCase();
	
	if(alreadyGuessed(word)){return}
	
	const response = await axios.post('/check', { params: {'word' : word}})
	const result = response.data.result
	showResult(result, word)
	$('input').val('')
}

/** updates highscore and number of plays on server */
async function updateHighscoreAndNumPlays(score){
	const response = await axios.post('/score', { params: {'new_score' : score}})
	const highScore = response.data.high_score
	const numOfPlays = response.data.num_plays
	updateInfo('num-plays', 'GAME#', numOfPlays)
	updateInfo('high-score', 'HIGHSCORE', highScore)
}

/**checks if word has already been guessed */
function alreadyGuessed(word){
	if (seenWords.includes(word)){
		generateAlert('info',`"${word}" has already been guessed`, 500)
		$('input').val('')
		return true
	} else{
		seenWords.push(word)
		return false
	}
}

/** generates an alert showing feedback on guess*/
function showResult(result, word){
	if(result === 'ok'){
		wordLen = word.length
		if(wordLen < 2){
			generateAlert('success',`${wordLen} POINT`, 300)
		}
		else {
			generateAlert('success',`${wordLen} POINTS`, 300)
		}
		calculateScore(word)
	}
	else if(result === 'not-on-board'){
		generateAlert('danger',`"${word}" not on board`, 500)
	}
	else if(result === 'not-word'){
		generateAlert('warning', `"${word}" is not a word`, 500)
	}
}

/**keeps track of current game's score */
function calculateScore(word){
	const word_score = word.length
	score += word_score
	updateInfo('score', 'SCORE', score)
}

/**game timer */
function timer(){
	time -= 1
	updateInfo('timer', 'TIME', time)
	if(time === 0){
		canPlay = false
		clearInterval(intervalID)
		updateHighscoreAndNumPlays(score)
	}
}

/** helper function to generate game info html */
function updateInfo(id, text, val){
	$(`#${id}`).html(`${text}: ${val}`)
}

/** helper function to generate HTML for alerts */
function generateAlert(type,msg,time){
	$('#alert-container').append(
		`<div id="alert" class="alert alert-${type}" role="alert">${msg}</div>`).css('display', 'block'
	);
	setTimeout(() => $('#alert').remove(), time)
}