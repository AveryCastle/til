const fs = require('fs');
const { statement } = require('./invoice'); // invoice.js에서 함수를 가져옴

// JSON 파일을 동기적으로 읽고 파싱
const invoice = JSON.parse(fs.readFileSync('invoices.json', 'utf8'));
const plays = JSON.parse(fs.readFileSync('plays.json', 'utf8'));

// statement 함수 호출
const result = statement(invoice[0], plays);
console.log(result);
