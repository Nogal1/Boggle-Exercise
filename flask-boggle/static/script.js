class BoggleGame {
    constructor(boardId, timerId, scoreId, resultId) {
        this.board = document.getElementById(boardId);
        this.timer = document.getElementById(timerId);
        this.score = document.getElementById(scoreId);
        this.result = document.getElementById(resultId);
        this.timeLeft = 60;
        this.scoreValue = 0;
        this.gameActive = true;  // Flag to track if the game is still active

        this.timerInterval = setInterval(this.tick.bind(this), 1000);
    }

    async submitWord(word) {
        if (!this.gameActive) return;  // Prevent word submission if the game is over

        const response = await axios.post("/check-word", { word });
        const result = response.data.result;
        this.showResult(result, word);
        if (result === "ok") this.updateScore(word.length);
    }

    showResult(result, word) {
        if (result === "ok") {
            this.result.innerText = `${word} is a valid word!`;
        } else if (result === "not-on-board") {
            this.result.innerText = `${word} is not on the board.`;
        } else {
            this.result.innerText = `${word} is not a valid word.`;
        }
    }

    updateScore(points) {
        this.scoreValue += points;
        this.score.innerText = `Score: ${this.scoreValue}`;
    }

    async tick() {
        this.timeLeft--;
        this.timer.innerText = `Time left: ${this.timeLeft} seconds`;

        if (this.timeLeft === 0) {
            this.endGame();
        }
    }

    async endGame() {
        this.gameActive = false;  // Set the game as inactive
        clearInterval(this.timerInterval);
        this.result.innerText = "Time's up!";
        await axios.post("/post-score", { score: this.scoreValue });
    }
}

// Initialize the game
const game = new BoggleGame("board", "timer", "score", "result");

