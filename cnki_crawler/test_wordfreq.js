if(process.argv.length < 3) {
    console.log('args: journal_id year');
    process.exit();
}
var journal_id = process.argv[2];
var year = process.argv[3];

var fs = require('fs');
var content = fs.readFileSync('./tag_clouds/' + journal_id + '_' + year + '_summary.txt', 'utf8');

WordFreqSync = require('./node_modules/wordfreq/src/wordfreq.worker.js')
var word_list = WordFreqSync().process(content).filter(function(word) {
    var stop_words = ['一个', '的'];
    var found_stop_words = stop_words.filter(function(stop_word) {
        return word[0].includes(stop_word);
    });
    return found_stop_words.length == 0;
});
top_word_list = word_list.slice(0, 20);

console.log(top_word_list);