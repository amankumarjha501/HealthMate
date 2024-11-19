function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    var chatBox = document.getElementById('chat-box');
    var userMessage = document.createElement('div');
    userMessage.className = 'user-message';
    userMessage.innerHTML = 'You: ' + userInput;
    chatBox.appendChild(userMessage);

    // Send user input to backend
    fetch('/sendMessage', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'user_input=' + encodeURIComponent(userInput),
    })
    .then(response => response.json())
    .then(data => {
        var botMessage = document.createElement('div');
        botMessage.className = 'bot-message';
        botMessage.innerHTML = 'HealthMate: ' + data.response;
        chatBox.appendChild(botMessage);

        // Clear input field after sending message
        document.getElementById('user-input').value = '';

        // Scroll to bottom of chat box
        chatBox.scrollTop = chatBox.scrollHeight;

        
    });
}
function sendMessage1(buttonElement) {
    const queryText = buttonElement.getAttribute('data-query');
    addMessageToChatBox('You: ' + queryText, 'user-message');

    const botResponse = getBotResponse(queryText);

    // Display the bot's response
    addMessageToChatBox('HealthMate: ' + botResponse, 'bot-message');
}

function getBotResponse(queryText) {
    switch (queryText) {
        case "Suffering from Viral Fever?":
            return getViralFeverResponse();
        case "Are you COVID Positive?":
            return getCovidResponse();
        case "Suffering with Glaucoma?":
            return getGlaucomaResponse();
        case "Bird Flu?":
            return getBirdFluResponse();
        default:
            return "<p>I'm sorry, I don't have information on that topic. Please try asking about something else.</p>";
    }
}

function getViralFeverResponse() {
    return `
        <p>I'm sorry to hear that you're dealing with a viral fever. Here's some information and advice to help you manage your symptoms and promote recovery:</p>
        <h4>Understanding Viral Fever</h4>
        <p>A viral fever is typically caused by an infection with a virus. Common types include the flu, the common cold, and other respiratory viruses. Symptoms may include:</p>
        <ul>
            <li>High temperature</li>
            <li>Chills</li>
            <li>Body aches</li>
            <li>Fatigue</li>
            <li>Headache</li>
            <li>Sore throat</li>
            <li>Cough</li>
            <li>Nasal congestion</li>
        </ul>
        <h4>General Care Tips</h4>
        <ul>
            <li><strong>Rest:</strong> Your body needs energy to fight off the infection. Ensure you get plenty of rest.</li>
            <li><strong>Hydration:</strong> Drink plenty of fluids such as water, herbal teas, and broths. Dehydration can worsen symptoms like headaches and fatigue.</li>
            <li><strong>Balanced Diet:</strong> Eat nutrient-rich foods like fruits, vegetables, and lean proteins to support your immune system.</li>
            <li><strong>Medication:</strong> Over-the-counter medications like acetaminophen or ibuprofen can help reduce fever and alleviate pain. Always follow the dosage instructions and consult a healthcare professional if you're unsure.</li>
            <li><strong>Cool Compress:</strong> Applying a cool, damp cloth to your forehead can help reduce fever.</li>
            <li><strong>Avoid Spreading the Virus:</strong> Stay isolated to prevent spreading the infection to others. Practice good hygiene, such as washing hands frequently and covering your mouth when coughing or sneezing.</li>
        </ul>
        <h4>When to See a Doctor</h4>
        <p>While most viral fevers can be managed at home, seek medical attention if you experience:</p>
        <ul>
            <li>A high fever that doesn’t respond to medication or lasts more than 3 days.</li>
            <li>Difficulty breathing or shortness of breath.</li>
            <li>Severe headache or neck stiffness.</li>
            <li>Persistent vomiting or diarrhea leading to dehydration.</li>
            <li>Rash or unusual symptoms.</li>
            <li>If you have a pre-existing condition that could be worsened by a fever.</li>
        </ul>
        <h4>Home Remedies</h4>
        <ul>
            <li><strong>Ginger Tea:</strong> Ginger has anti-inflammatory properties that may help reduce symptoms. Boil some ginger in water, strain, and add honey.</li>
            <li><strong>Honey and Lemon:</strong> Mix honey and lemon in warm water to soothe a sore throat.</li>
            <li><strong>Steam Inhalation:</strong> Inhale steam from a bowl of hot water to relieve congestion. Be cautious to avoid burns.</li>
            <li><strong>Gargling with Salt Water:</strong> This can help reduce throat inflammation and kill bacteria.</li>
        </ul>
        <h4>Prevention</h4>
        <ul>
            <li><strong>Vaccination:</strong> Keep up with recommended vaccinations, including the flu shot.</li>
            <li><strong>Hygiene:</strong> Regular hand washing and avoiding close contact with sick individuals can reduce the risk of infection.</li>
            <li><strong>Healthy Lifestyle:</strong> Maintain a balanced diet, regular exercise, and adequate sleep to keep your immune system strong.</li>
        </ul>
        <h4>Important Notes</h4>
        <ul>
            <li><strong>Avoid Antibiotics:</strong> Viral infections do not respond to antibiotics, which are only effective against bacterial infections.</li>
            <li><strong>Monitor Symptoms:</strong> Keep track of your symptoms. If there’s any sudden worsening or new symptoms appear, consult a healthcare provider.</li>
        </ul>
        <p>Most viral fevers resolve on their own with proper care. Following these tips can help alleviate symptoms and speed up recovery. If in doubt, don’t hesitate to seek medical advice.</p>
        <p>Feel better soon! If you have any more questions or need further information, feel free to ask.</p>
    `;
}

function getCovidResponse() {
    return `
        <p>I'm really sorry to hear that you've tested positive for COVID-19. It's important to take care of yourself and follow appropriate guidelines to manage your symptoms and prevent spreading the virus to others. Here’s some detailed advice on how to manage your condition:</p>
        <h4>Immediate Steps to Take</h4>
        <ul>
            <li><strong>Isolate Yourself:</strong>
                <ul>
                    <li>Stay in a separate room away from other household members.</li>
                    <li>Use a separate bathroom if possible.</li>
                    <li>Avoid sharing personal items such as utensils, towels, and bedding.</li>
                </ul>
            </li>
            <li><strong>Inform Close Contacts:</strong>
                <ul>
                    <li>Notify people you’ve been in contact with recently so they can monitor their health and take necessary precautions.</li>
                </ul>
            </li>
            <li><strong>Monitor Symptoms:</strong>
                <ul>
                    <li>Keep track of your symptoms. Common symptoms include fever, cough, and loss of taste or smell. Severe symptoms can include difficulty breathing and chest pain.</li>
                </ul>
            </li>
        </ul>
        <h4>Home Care and Symptom Management</h4>
        <ul>
            <li><strong>Rest and Hydration:</strong>
                <ul>
                    <li>Get plenty of rest to help your body fight the virus.</li>
                    <li>Drink fluids like water, herbal teas, and broths to stay hydrated.</li>
                </ul>
            </li>
            <li><strong>Nutrition:</strong>
                <ul>
                    <li>Eat a balanced diet rich in fruits, vegetables, and proteins to support your immune system.</li>
                </ul>
            </li>
            <li><strong>Over-the-Counter Medications:</strong>
                <ul>
                    <li>Use medications like acetaminophen or ibuprofen to reduce fever and relieve aches and pains. Follow the dosage instructions and consult with a healthcare professional if you have any questions.</li>
                </ul>
            </li>
            <li><strong>Breathing Exercises:</strong>
                <ul>
                    <li>Practice deep breathing exercises to help keep your lungs clear and functioning properly.</li>
                </ul>
            </li>
            <li><strong>Ventilate Your Room:</strong>
                <ul>
                    <li>Keep windows open to ensure good air circulation and reduce the concentration of the virus in the air.</li>
                </ul>
            </li>
            <li><strong>Use a Humidifier:</strong>
                <ul>
                    <li>This can help maintain moisture in the air, which might ease coughs and sore throats.</li>
                </ul>
            </li>
        </ul>
        <h4>When to Seek Medical Attention</h4>
        <p>Contact a healthcare provider if you experience any of the following:</p>
        <ul>
            <li>Difficulty breathing or shortness of breath.</li>
            <li>Persistent chest pain or pressure.</li>
            <li>Confusion or inability to stay awake.</li>
            <li>Bluish lips or face.</li>
            <li>Severe weakness or symptoms that worsen over time.</li>
        </ul>
        <h4>Preventing the Spread of COVID-19</h4>
        <ul>
            <li><strong>Wear a Mask:</strong>
                <ul>
                    <li>Wear a mask if you need to be around other people, even at home.</li>
                </ul>
            </li>
            <li><strong>Hand Hygiene:</strong>
                <ul>
                    <li>Wash your hands frequently with soap and water for at least 20 seconds.</li>
                    <li>Use hand sanitizer with at least 60% alcohol if soap and water aren’t available.</li>
                </ul>
            </li>
            <li><strong>Disinfect Surfaces:</strong>
                <ul>
                    <li>Regularly clean and disinfect high-touch surfaces like doorknobs, light switches, and cell phones.</li>
                </ul>
            </li>
        </ul>
        <h4>Recovery and Post-COVID Care</h4>
        <ul>
            <li><strong>Follow Up with Healthcare Providers:</strong>
                <ul>
                    <li>Consult your doctor for a follow-up to ensure your recovery is on track and to address any lingering symptoms.</li>
                </ul>
            </li>
            <li><strong>Gradual Return to Activity:</strong>
                <ul>
                    <li>Ease back into your regular activities and listen to your body. Avoid strenuous activities until you’re fully recovered.</li>
                </ul>
            </li>
        </ul>
        <p>Remember, COVID-19 affects people differently, so it’s important to monitor your symptoms closely and seek medical advice if necessary. Stay safe and take care. If you have any more questions or need further information, don’t hesitate to ask.</p>
    `;
}

function getGlaucomaResponse() {
    return `
        <p>Glaucoma is a serious condition that affects the eyes, leading to damage to the optic nerve. It’s essential to manage and treat glaucoma properly to prevent further damage and potential vision loss. Here’s what you need to know:</p>
        <h4>Understanding Glaucoma</h4>
        <p>Glaucoma is usually caused by increased pressure within the eye, known as intraocular pressure (IOP). This pressure can damage the optic nerve, which is crucial for vision. There are several types of glaucoma, with the most common being:</p>
        <ul>
            <li><strong>Open-Angle Glaucoma:</strong> The most common form, where the drainage angle for eye fluid appears normal, but the fluid doesn’t flow out as it should.</li>
            <li><strong>Angle-Closure Glaucoma:</strong> A less common form where the eye’s drainage angle becomes blocked, leading to a rapid increase in eye pressure.</li>
            <li><strong>Normal-Tension Glaucoma:</strong> Even without high IOP, optic nerve damage can occur.</li>
        </ul>
        <h4>Symptoms of Glaucoma</h4>
        <ul>
            <li>Gradual loss of peripheral vision, usually in both eyes.</li>
            <li>Advanced stages can lead to tunnel vision.</li>
            <li>For angle-closure glaucoma, symptoms can include severe eye pain, nausea, vomiting, and sudden visual disturbance.</li>
        </ul>
        <h4>Treatment Options</h4>
        <p>Glaucoma treatments focus on lowering eye pressure to prevent further damage. Options include:</p>
        <ul>
            <li><strong>Medications:</strong>
                <ul>
                    <li>Eye drops or oral medications can help decrease eye pressure by improving fluid outflow or reducing fluid production.</li>
                </ul>
            </li>
            <li><strong>Laser Treatment:</strong>
                <ul>
                    <li>Laser trabeculoplasty helps improve fluid drainage.</li>
                    <li>Laser iridotomy creates a small opening in the iris to improve fluid flow in angle-closure glaucoma.</li>
                </ul>
            </li>
            <li><strong>Surgery:</strong>
                <ul>
                    <li>Trabeculectomy involves creating a new drainage path for eye fluid.</li>
                    <li>Implanting drainage devices can also help fluid escape from the eye.</li>
                </ul>
            </li>
        </ul>
        <h4>Managing Glaucoma</h4>
        <p>Managing glaucoma requires regular eye exams and adherence to treatment plans. Here’s how you can manage the condition:</p>
        <ul>
            <li><strong>Regular Eye Check-Ups:</strong>
                <ul>
                    <li>Visit your eye doctor regularly to monitor your eye pressure and optic nerve health.</li>
                </ul>
            </li>
            <li><strong>Medication Adherence:</strong>
                <ul>
                    <li>Take prescribed eye drops and medications consistently to control eye pressure.</li>
                </ul>
            </li>
            <li><strong>Healthy Lifestyle:</strong>
                <ul>
                    <li>Maintain a balanced diet rich in nutrients beneficial for eye health, such as leafy greens and omega-3 fatty acids.</li>
                    <li>Exercise regularly to support overall health and potentially lower eye pressure.</li>
                </ul>
            </li>
            <li><strong>Protect Your Eyes:</strong>
                <ul>
                    <li>Avoid activities that might cause eye injury and wear protective eyewear if necessary.</li>
                </ul>
            </li>
            <li><strong>Monitor Symptoms:</strong>
                <ul>
                    <li>Be aware of changes in your vision or new symptoms, and report them to your eye doctor immediately.</li>
                </ul>
            </li>
        </ul>
        <h4>Living with Glaucoma</h4>
        <p>While glaucoma can’t be cured, early diagnosis and proper management can preserve vision and improve quality of life. Stay informed about your condition and work closely with your healthcare providers to keep your eyes healthy.</p>
        <p>If you have any more questions or need further information, don’t hesitate to ask. Take care and stay proactive about your eye health.</p>
    `;
}

function getBirdFluResponse() {
    return `
        <p>Bird flu, also known as avian influenza, is a viral infection that primarily affects birds but can occasionally infect humans. Here’s some important information on how to recognize and manage bird flu:</p>
        <h4>Understanding Bird Flu</h4>
        <p>Bird flu viruses can be classified into two categories:</p>
        <ul>
            <li><strong>Low Pathogenic Avian Influenza (LPAI):</strong> Causes mild symptoms in birds and rarely infects humans.</li>
            <li><strong>Highly Pathogenic Avian Influenza (HPAI):</strong> Can cause severe disease in birds and poses a higher risk to humans.</li>
        </ul>
        <h4>Symptoms of Bird Flu</h4>
        <p>In humans, bird flu symptoms can range from mild to severe and include:</p>
        <ul>
            <li>Fever and chills</li>
            <li>Cough and sore throat</li>
            <li>Muscle aches</li>
            <li>Shortness of breath</li>
            <li>Conjunctivitis (eye infection)</li>
            <li>In severe cases, symptoms can progress to pneumonia, acute respiratory distress, and even death.</li>
        </ul>
        <h4>Prevention and Treatment</h4>
        <ul>
            <li><strong>Avoid Contact with Infected Birds:</strong>
                <ul>
                    <li>Do not handle birds that appear sick or have died from unknown causes.</li>
                </ul>
            </li>
            <li><strong>Practice Good Hygiene:</strong>
                <ul>
                    <li>Wash hands frequently with soap and water.</li>
                    <li>Use hand sanitizer if soap and water are unavailable.</li>
                </ul>
            </li>
            <li><strong>Cook Poultry Thoroughly:</strong>
                <ul>
                    <li>Ensure poultry and eggs are cooked to a safe internal temperature to kill any viruses.</li>
                </ul>
            </li>
            <li><strong>Vaccination:</strong>
                <ul>
                    <li>Seasonal flu vaccines do not protect against bird flu, but getting vaccinated can reduce the risk of co-infection with human and bird flu viruses.</li>
                </ul>
            </li>
            <li><strong>Antiviral Medications:</strong>
                <ul>
                    <li>Infected individuals may be treated with antiviral medications such as oseltamivir (Tamiflu) or zanamivir (Relenza) to reduce symptoms and prevent complications.</li>
                </ul>
            </li>
        </ul>
        <h4>When to Seek Medical Attention</h4>
        <p>If you develop symptoms of bird flu and have had recent contact with birds or traveled to an area affected by avian influenza, seek medical attention promptly. Early diagnosis and treatment are crucial for managing the infection and preventing complications.</p>
        <p>Stay informed about bird flu outbreaks and take appropriate precautions to protect yourself and your family. If you have any more questions or need further information, feel free to ask.</p>
    `;
}

function addMessageToChatBox(message, className) {
    var chatBox = document.getElementById('chat-box');
    var messageDiv = document.createElement('div');
    messageDiv.className = className;
    messageDiv.innerHTML = message;
    chatBox.appendChild(messageDiv);

    // Scroll to bottom of chat box
    chatBox.scrollTop = chatBox.scrollHeight;
}




document.getElementById('user-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

document.getElementById('message-form').addEventListener('submit', function(event) {
    event.preventDefault();
    sendMessage();
});
