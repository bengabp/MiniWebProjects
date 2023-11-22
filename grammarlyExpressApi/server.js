import express from "express";
import { correct, Grammarly } from "@stewartmcgown/grammarly-api";

async function grammarly_correct(sentence){
    const { corrected } = await new Grammarly().analyse(sentence).then(correct);
    return corrected;
}

// Create an express app
const app = express();

app.get("/",(request,response)=>{
    response.send("<h1>Express apis</h1>")
});

app.get("/text-processors/grammarly-correct-text-content",async (request,response)=>{
    const text_content = request.query.text_content;
    const corrected_text_content = await grammarly_correct(text_content);

    console.log("ORIGINAL TEXT : ",text_content)
    console.log("CORRECTED : ",corrected_text_content,"\n");

    response.json({
        original_text_content:text_content,
        corrected_text_content:corrected_text_content
    })
});

app.listen(3000,()=>{console.log("Server started,listening on port 3000")})
