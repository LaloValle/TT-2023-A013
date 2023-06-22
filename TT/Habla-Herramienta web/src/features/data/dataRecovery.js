import { phonemes, gestures } from '../../content'

// When a query is passed the complete list gets filtered(search)
export const getPhonemes = async (query='') => {
  await fakeLatency()
  return query == ''
          ? phonemes
          : phonemes // The search must be applied
}

// When a query is passed the complete list gets filtered(search)
export const getGestures = async (query='') => {
  await fakeLatency()
  return query == ''
          ? gestures.es
          : gestures.es // The search must be applied
}

// Auxiliar function that mimics the latency behaviour in a real network environment
const fakeLatency = async () => {
  return new Promise(res => {
    setTimeout(res, Math.random() * 800);
  });
}