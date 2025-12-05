import { dummyUser } from '../utils/dummy-data.js';

export async function login(payload) {
  return {
    ...dummyUser,
    email: payload.email,
  };
}

export async function signup(payload) {
  return {
    ...dummyUser,
    name: payload.name,
    email: payload.email,
    phone: payload.phone,
  };
}

export async function logout() {
  return true;
}

export async function getCurrentUser() {
  return null;
}
