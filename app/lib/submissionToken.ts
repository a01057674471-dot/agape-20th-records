import "server-only";

function secret() {
  const value = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!value) throw new Error("자료 관리 서명키가 없습니다.");
  return value;
}

function bytesToHex(bytes: ArrayBuffer) {
  return Array.from(new Uint8Array(bytes))
    .map((byte) => byte.toString(16).padStart(2, "0"))
    .join("");
}

async function signature(id: string) {
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret()),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  return bytesToHex(await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(id)));
}

export async function createSubmissionToken(id: string) {
  return signature(id);
}

export async function verifySubmissionToken(id: string, token: string | null) {
  if (!token || token.length !== 64) return false;
  const expected = await signature(id);
  let difference = 0;
  for (let index = 0; index < expected.length; index += 1) {
    difference |= expected.charCodeAt(index) ^ token.charCodeAt(index);
  }
  return difference === 0;
}
