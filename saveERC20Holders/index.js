const fs = require("fs");

// Replace with your own data
// You can get the data from the Etherscan API or directly from Infura/Moralis.
const data = [
  {
    TokenHolderAddress: "address_here",
    TokenHolderQuantity: "token_balance_here",
  },
];

function formatData(data) {
  return data
    .map((entry) => {
      // You can remove this variable if the token amount doesn't have 18 decimals.
      const formattedQuantity =
        BigInt(entry.TokenHolderQuantity) / BigInt(10 ** 18);
      return `${entry.TokenHolderAddress}: ${formattedQuantity.toString()}`;
    })
    .join("\n");
}

const formattedData = formatData(data);
fs.writeFileSync("token_holders.txt", formattedData);
console.log("Data saved to token_holders.txt");
