import re


def remove_disclaimer(text):
    pattern = r"^(.*?)(DISCLAIMER:)"

    match = re.search(pattern, text, re.DOTALL)

    if match:
        # Extract everything before DISCLAIMER
        text_before_disclaimer = match.group(1).strip()

        return text_before_disclaimer
    else:
        return text

    # Your article text


demo_article = "Your article text here DISCLAIMER: This is the disclaimer text."


big_artice = """
INFO:

Rosemary (Rosmarinus officinalis) is a fragrant evergreen herb native to the Mediterranean region. It is used in cooking for its flavor and has a long history of use in traditional medicine.

Scientific research has suggested that rosemary may have several health benefits, which include:

Antioxidant Properties: Rosemary contains compounds such as carnosic acid and rosmarinic acid that have antioxidant properties, which can help protect the body's cells from damage by free radicals.

Anti-inflammatory Effects: The same compounds that give rosemary its antioxidant benefits also contribute to its anti-inflammatory properties, which may help reduce inflammation in the body.

Cognitive Enhancement: Studies have shown that rosemary can have a positive effect on cognitive performance. Its aroma, in particular, has been linked to improved concentration, performance, speed, and accuracy in cognitive tasks.

Neuroprotective Potential: Some research suggests that rosemary may be beneficial for brain health and could protect against neurodegenerative diseases like Alzheimer's disease, although more research is needed to confirm this effect.

Antimicrobial Activity: Extracts from rosemary have been found to have antimicrobial properties, which means they can help inhibit the growth of bacteria and fungi.

Mechanisms of action for rosemary's medicinal benefits are thought to be linked to its bioactive compounds, which can interact with the body in various ways. For example, carnosic acid is believed to protect neurons from oxidative stress, and rosmarinic acid may modulate inflammation through its effects on various signaling pathways in the body.

DISCLAIMER:

It's important to note that while there is promising research on rosemary's potential health benefits, many studies are preliminary or have been conducted in vitro (in a laboratory setting) or in animals. More extensive clinical trials in humans are needed to fully understand the effects and confirm the efficacy of rosemary as a therapeutic agent.

Additionally, rosemary should be used with caution, as high doses can lead to potential side effects, and it can interact with certain medications. Rosemary essential oil, in particular, is potent and should not be taken internally without the supervision of a healthcare professional.

Always consult with a healthcare provider before starting any new treatment or herbal supplementation to ensure it is safe and appropriate for your specific health condition.

"""

print(remove_disclaimer(big_artice))
