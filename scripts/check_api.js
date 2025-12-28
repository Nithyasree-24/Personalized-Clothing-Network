const https = require('https');

const url = 'https://fakeapi.platzi.com/products';

const req = https.get(url, (res) => {
  console.log('statusCode:', res.statusCode);
  console.log('content-type:', res.headers['content-type']);
  let chunks = [];
  res.on('data', (d) => chunks.push(d));
  res.on('end', () => {
    const body = Buffer.concat(chunks).toString('utf8');
    console.log('\n--- body start ---\n');
    console.log(body.slice(0, 2000));
    console.log('\n--- body end (truncated) ---\n');
  });
});

req.on('error', (e) => {
  console.error('request error:', e.message);
});

req.setTimeout(10000, () => {
  console.error('request timed out');
  req.abort();
});
