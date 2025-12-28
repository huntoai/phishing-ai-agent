// Course and Lesson Data for Awareness Training
export const courses = [
  {
    id: 'basics',
    title: 'Phishing Basics',
    description: 'Learn the fundamentals of phishing and how to identify common attacks',
    icon: '🎯',
    level: 'Beginner',
    estimatedTime: '15 min',
    lessons: 8,
  },
  {
    id: 'email',
    title: 'Email Phishing',
    description: 'Master email phishing detection and protection techniques',
    icon: '📧',
    level: 'Intermediate',
    estimatedTime: '20 min',
    lessons: 10,
  },
  {
    id: 'sms',
    title: 'SMS & Smishing',
    description: 'Identify and protect against SMS-based phishing attacks',
    icon: '💬',
    level: 'Intermediate',
    estimatedTime: '15 min',
    lessons: 7,
  },
  {
    id: 'social',
    title: 'Social Media Scams',
    description: 'Navigate social media safely and spot scam attempts',
    icon: '📱',
    level: 'Intermediate',
    estimatedTime: '20 min',
    lessons: 9,
  },
  {
    id: 'advanced',
    title: 'Advanced Threats',
    description: 'Learn about sophisticated phishing and social engineering',
    icon: '🎓',
    level: 'Advanced',
    estimatedTime: '25 min',
    lessons: 12,
  },
];

export const lessons = {
  basics: [
    {
      id: 'basics-1',
      title: 'What is Phishing?',
      description: 'Understanding the basics of phishing attacks',
      points: 10,
      type: 'theory',
      content: {
        text: `Phishing is a type of cyber attack where criminals attempt to trick you into revealing sensitive information like passwords, credit card numbers, or personal data.

These attacks often come disguised as:
• Legitimate emails from banks or companies
• Urgent messages requiring immediate action
• Offers that seem too good to be true
• Messages from people you trust

The goal is to steal your information or install malware on your device.`,
        examples: [
          'Fake bank emails asking you to verify your account',
          'Messages claiming you won a prize',
          'Urgent requests to update payment information',
        ],
      },
      quiz: [
        {
          question: 'What is the main goal of phishing attacks?',
          options: [
            'To steal your personal information',
            'To send you spam',
            'To test your email service',
            'To improve security',
          ],
          correct: 0,
        },
        {
          question: 'Which of these is a common phishing tactic?',
          options: [
            'Sending helpful information',
            'Creating a sense of urgency',
            'Being completely transparent',
            'Asking for nothing',
          ],
          correct: 1,
        },
      ],
    },
    {
      id: 'basics-2',
      title: 'Red Flags to Watch For',
      description: 'Learn to identify suspicious messages',
      points: 15,
      type: 'interactive',
      content: {
        text: `Learning to spot red flags can save you from falling victim to phishing. Here are key warning signs:

1. **Suspicious Sender**: Check the email address carefully
2. **Generic Greetings**: "Dear Customer" instead of your name
3. **Urgent Language**: Threats or pressure to act immediately
4. **Spelling Errors**: Poor grammar or unusual formatting
5. **Suspicious Links**: Hover to see where they actually lead
6. **Requests for Information**: Legitimate companies won't ask for passwords via email`,
      },
      quiz: [
        {
          question: 'An email starts with "Dear Valued Customer". Is this a red flag?',
          options: [
            'Yes, legitimate companies usually use your name',
            'No, this is normal',
            'Only if it asks for money',
            'No red flag at all',
          ],
          correct: 0,
        },
        {
          question: 'What should you do before clicking a link in an email?',
          options: [
            'Click it immediately',
            'Hover over it to see the actual URL',
            'Forward the email',
            'Delete the email without checking',
          ],
          correct: 1,
        },
        {
          question: 'An email threatens to close your account if you don\'t act now. What is this?',
          options: [
            'A legitimate warning',
            'A phishing tactic using urgency',
            'Standard procedure',
            'Good customer service',
          ],
          correct: 1,
        },
      ],
    },
  ],
  // More lessons can be added here for other courses
};

export default { courses, lessons };
