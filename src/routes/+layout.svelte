<script lang="ts">
	import 'carbon-components-svelte/css/g100.css';
	import '@carbon/charts/styles.css';
	import {
		Header,
		HeaderUtilities,
		HeaderAction,
		HeaderPanelLinks,
		HeaderPanelDivider,
		HeaderPanelLink,
		Content,
		Grid,
		Row,
		Column,
		Link,
		OutboundLink
	} from 'carbon-components-svelte';
	import { onMount } from 'svelte';

	let isOpen = false;
	let transition = { duration: 200 };

	function url_builder(href: string) {
		console.log(token);
		if (token !== null) {
			return href + '?token=' + token;
		}
		return href;
	}

	let token: string | null;
	onMount(() => {
		token = new URL(document.location).searchParams.get('token');
	});
</script>

<Header company="Magpie" platformName="Mail">
	<HeaderUtilities>
		<HeaderAction bind:isOpen {transition}>
			<HeaderPanelLinks>
				<HeaderPanelLink>
					<Link href={url_builder('/')}>Home</Link>
				</HeaderPanelLink>
				<HeaderPanelDivider>Internal Apps</HeaderPanelDivider>
				<HeaderPanelLink>
					<Link href={url_builder('/internal/operational_dashboard')}>Operational Dashboard</Link>
				</HeaderPanelLink>
				<HeaderPanelLink>
					<Link href={url_builder('/internal/customer_service')}>Customer Service</Link>
				</HeaderPanelLink>
				<HeaderPanelDivider>External Apps</HeaderPanelDivider>
				<HeaderPanelLink>
					<Link href={url_builder('/external/parcel_tracker')}>Parcel Tracker</Link>
				</HeaderPanelLink>
				<HeaderPanelLink>
					<Link href={url_builder('/external/parcel_order')}>Parcel Order</Link>
				</HeaderPanelLink>
				<HeaderPanelDivider>Other</HeaderPanelDivider>
				<HeaderPanelLink>
					<OutboundLink href="https://github.com/sdairs/gsd_delivery_demo">GitHub Repo</OutboundLink
					>
				</HeaderPanelLink>
				<HeaderPanelLink>
					<OutboundLink href="https://tinybird.co">Tinybird</OutboundLink>
				</HeaderPanelLink>
				<HeaderPanelLink>
					<OutboundLink
						href="https://analytics.tinybird.co/?token=p.eyJ1IjogIjMwZjM3YTdkLTEyMjYtNDcxYi1hM2ZjLTZhZjc2MGNmNTBiMSIsICJpZCI6ICJlZmI1NTNkMy1hOTM0LTRmZDgtYTE3ZC1hYzQzOTVlZTdiOTEifQ._LUtvgNPQ-npnhNSARML7uVkvI2MUSW2C35htot5J0A&host=https://api.tinybird.co"
						>Web Analytics</OutboundLink
					>
				</HeaderPanelLink>
			</HeaderPanelLinks>
		</HeaderAction>
	</HeaderUtilities>
</Header>

<Content>
	<Grid>
		<Row>
			<Column>
				<slot />
			</Column>
		</Row>
	</Grid>
</Content>
