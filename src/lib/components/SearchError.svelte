<script lang="ts">
	import { InlineNotification } from 'carbon-components-svelte';

	export let error_message: string;
</script>

<InlineNotification title="Error:" subtitle="{error_message}" />
