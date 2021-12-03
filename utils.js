const crypto = require("crypto");

/**
 * @param {Number} len - Length of the token to be generated
 * @returns {String} Alphanumeric random token
 */
function tokenGenerator(len = 16) {
  const numerals = "0123456789";
  const lowercase_letters = "abcdefghijklmnopqrstuvwxyz";
  const uppercase_letters = lowercase_letters.toUpperCase();
  const options = [numerals, lowercase_letters, uppercase_letters];
  const token = Array(len)
    .fill()
    .map((v, i) => {
      const option = options[crypto.randomInt(3)];
      const random_char = option.charAt(crypto.randomInt(option.length));
      return random_char;
    })
    .join("");
  return token;
}

module.exports = { tokenGenerator };
