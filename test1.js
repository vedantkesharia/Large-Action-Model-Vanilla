const { AzureOpenAI } = require("openai");

// Load the .env file if it exists
const dotenv = require("dotenv");
dotenv.config();

// You will need to set these environment variables or edit the following values
const endpoint = process.env["AZURE_OPENAI_ENDPOINT"] || "<endpoint>";
const apiKey = process.env["AZURE_OPENAI_API_KEY"] || "<api key>";
const apiVersion = "2024-05-01-preview";
const deployment = "Gpt4o"; // This must match your deployment name.

async function main() {
  const client = new AzureOpenAI({ endpoint, apiKey, apiVersion, deployment });

  const result = await client.chat.completions.create({
    messages: [
      { role: "system", content: "You are a helpful assistant." },
      { role: "user", content: "Does Azure OpenAI support customer managed keys?" },
      { role: "assistant", content: "Yes, customer managed keys are supported by Azure OpenAI?" },
      { role: "user", content: "Do other Azure AI services support this too?" },
    ],
    model: "",
  });

  // Print just the output content
  console.log(result.choices[0].message.content);
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});