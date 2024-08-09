class BoggleGame {
    /* make a new game at this DOM id */

    constructor(boardId, secs = 60) {
        this.secs = secs;
        this.score = 0;
        this.words = new Set();
        this.board = $("#" + boardId);

        this.showTimer();
        this.timer = setInterval(this.tick.bind(this), 1000);
        this.board.on("submit", ".add-word", this.handleSubmit.bind(this));
    }

    /* show word in list of words */

    showWord(word) {
        this.appendToBoard(".words", $("<li>", { text: word }));
    }

    /* show score in html */

    showScore() {
        this.updateBoardText(".score", this.score);
    }

    /* show a status message */

    showMessage(msg, cls) {
        const msgElement = $(".msg", this.board);
        msgElement.text(msg).removeClass().addClass(`msg ${cls}`);
    }

    /* handle submission of word: if unique and valid, score & show */

    async handleSubmit(evt) {
        evt.preventDefault();
        const $word = this.getWordElement();

        const word = $word.val().trim();
        if (!word || this.words.has(word)) {
            this.handleInvalidWord(word);
            return;
        }

        const response = await this.checkWordWithServer(word);
        this.processWordCheck(response, word);

        this.resetWordInput($word);
    }

    /* Update timer in DOM */

    showTimer() {
        this.updateBoardText(".timer", this.secs);
    }

    /* Tick: handle a second passing in game */

    async tick() {
        this.secs--;
        this.showTimer();

        if (this.secs <= 0) {
            clearInterval(this.timer);
            await this.endGame();
        }
    }

    /* end of game: score and update message. */

    async endGame() {
        $(".add-word", this.board).hide();
        const response = await this.postFinalScore();
        const message = response.data.brokeRecord
            ? `New record: ${this.score}`
            : `Final score: ${this.score}`;
        this.showMessage(message, "ok");
    }

    /* Helper methods */

    appendToBoard(selector, element) {
        $(selector, this.board).append(element);
    }

    updateBoardText(selector, text) {
        $(selector, this.board).text(text);
    }

    getWordElement() {
        return $(".word", this.board);
    }

    handleInvalidWord(word) {
        const message = this.words.has(word)
            ? `Already found ${word}`
            : `${word} is not a valid input`;
        this.showMessage(message, "err");
    }

    async checkWordWithServer(word) {
        return await axios.get("/check-word", { params: { word } });
    }

    processWordCheck(response, word) {
        const result = response.data.result;

        if (result === "ok") {
            this.addWordToGame(word);
        } else {
            this.showMessage(this.getErrorMessage(result, word), "err");
        }
    }

    addWordToGame(word) {
        this.showWord(word);
        this.score += word.length;
        this.showScore();
        this.words.add(word);
        this.showMessage(`Added: ${word}`, "ok");
    }

    resetWordInput($word) {
        $word.val("").focus();
    }

    async postFinalScore() {
        return await axios.post("/post-score", { score: this.score });
    }

    getErrorMessage(result, word) {
        if (result === "not-word") {
            return `${word} is not a valid English word`;
        } else if (result === "not-on-board") {
            return `${word} is not a valid word on this board`;
        }
        return "An error occurred";
    }
}
