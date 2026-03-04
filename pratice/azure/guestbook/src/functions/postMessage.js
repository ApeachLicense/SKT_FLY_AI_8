const { app } = require('@azure/functions');
const store = require('../store');

app.http('postMessage', {
    methods: ['POST'],
    authLevel: 'anonymous',
    route: 'api/messages',
    handler: async (request, context) => {
        try {
            const body = await request.json();
            const { name, message } = body;

            if (!name || !message) {
                return { status: 400, body: '이름과 메시지가 필요합니다.' };
            }

            store.addMessage({ name, message });
            return { status: 201, body: '메시지가 추가되었습니다.' };
        } catch (error) {
            context.error(error);
            return { status: 400, body: '유효하지 않은 JSON' };
        }
    }
});
