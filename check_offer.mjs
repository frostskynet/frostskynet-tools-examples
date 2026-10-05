// Public-only example. No wallets, .env files, credentials, signing, or paid retries.
const url = 'https://route-a-worker.frostskynet-api.workers.dev/clean';
try {
  const response = await fetch(url, {
    method: 'POST', redirect: 'error', signal: AbortSignal.timeout(15000),
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ input: 'First example line\nSecond example line', options: { minChars: 3 } }),
  });
  const header = response.headers.get('payment-required');
  const required = header && header.length <= 200000 ? JSON.parse(Buffer.from(header, 'base64').toString('utf8')) : null;
  const matches = response.status === 402 && required?.x402Version === 2 && required.accepts?.length === 1 && required.accepts.every(offer =>
    offer.scheme === 'exact' && offer.network === 'eip155:8453' && offer.amount === '5000' &&
    offer.asset?.toLowerCase() === '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913' &&
    offer.payTo?.toLowerCase() === '0x3a1121e787586a504ff74fc53e3acee19fade698');
  console.log(`HTTP status: ${response.status}`);
  console.log(`Expected payment terms: ${Boolean(matches)}`);
  try { await response.body?.cancel(); } catch {}
  process.exitCode = matches ? 0 : 1;
} catch {
  console.error('Unpaid offer check failed; raw diagnostics suppressed. No payment was sent.');
  process.exitCode = 1;
}
